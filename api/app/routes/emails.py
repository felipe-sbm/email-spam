from flask import Blueprint, request, jsonify
from app.services import spam_service, email_service
from datetime import datetime
import os

bp = Blueprint('emails', __name__)

@bp.route('/send', methods=['POST'])
def send_message():
    """
    Verifica se é spam e envia a mensagem se permitido.
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Campo "message" é obrigatório'}), 400
        
        message = data['message']
        recipient = data.get('recipient', 'default@example.com')
        
        if not isinstance(message, str) or not message.strip():
            return jsonify({'error': 'Mensagem inválida'}), 400
        
        # Fazer predição
        result = spam_service.predict(message)
        
        # Se for spam, bloquear
        if result['label'] == 'spam':
            return jsonify({
                'status': 'blocked',
                'reason': 'Mensagem identificada como spam',
                'confidence': result['confidence'],
                'message': message[:100] + '...' if len(message) > 100 else message
            }), 403
        
        # Se for ham, simular envio e salvar
        try:
            email_service.create_email(
                sender='me@example.com',
                recipient=recipient,
                subject=('(sent) ' + message[:60]) if message else '(sent)',
                body=message,
                is_spam=(result['label'] == 'spam'),
                spam_score=result.get('confidence', 0.0)
            )
        except Exception:
            pass
            
        return jsonify({
            'status': 'sent',
            'message_id': f"msg_{os.urandom(8).hex()}",
            'recipient': recipient,
            'message': message[:100] + '...' if len(message) > 100 else message,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao enviar mensagem', 'details': str(e)}), 500

@bp.route('/emails', methods=['GET'])
def list_emails():
    """List all stored emails"""
    try:
        records = email_service.get_all_emails()
        return jsonify([r.to_dict() for r in records]), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao listar emails', 'details': str(e)}), 500

@bp.route('/emails', methods=['POST'])
def create_email():
    """Create/store an email record"""
    try:
        data = request.get_json() or {}
        sender = data.get('sender', 'unknown')
        recipient = data.get('recipient', 'unknown')
        subject = data.get('subject', '')
        body = data.get('body', '')
        received = data.get('received')
        is_spam = bool(data.get('is_spam', False))
        spam_score = float(data.get('spam_score', 0.0))

        if received:
            try:
                received_dt = datetime.fromisoformat(received)
            except Exception:
                received_dt = datetime.now()
        else:
            received_dt = datetime.now()

        rec = email_service.create_email(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            received=received_dt,
            is_spam=is_spam,
            spam_score=spam_score
        )
        return jsonify(rec.to_dict()), 201

    except Exception as e:
        return jsonify({'error': 'Erro ao criar email', 'details': str(e)}), 500
