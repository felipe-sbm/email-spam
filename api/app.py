# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from spam_detector import SpamDetector
import pathlib
import sys

try:
    from models import db, EmailRecord
except ModuleNotFoundError as e:
    # Mensagem amigável para ajudar a resolver o ambiente sem mostrar stacktrace grande
    print("\nErro: dependência ausente ao tentar importar o módulo 'models'.\n")
    print("Provavelmente você está executando sem ativar o virtualenv do projeto '.venv'.")
    print("Para consertar, execute (no macOS / zsh):\n")
    print("    cd /Users/samuel/Documents/dev/email-spam/api")
    print("    python3 -m venv .venv  # se ainda não existir")
    print("    . .venv/bin/activate")
    print("    pip install -r requirements.txt\n")
    print("Ou instale a dependência específica globalmente: 'pip install Flask-SQLAlchemy' (não recomendado para desenvolvimento).\n")
    print("Saindo para que você possa ajustar o ambiente. Rode 'python3 app.py' novamente após instalar as dependências.\n")
    sys.exit(1)
import os
from datetime import datetime

app = Flask(__name__)
# Database configuration (SQLite file inside project)
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / 'emails.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH.as_posix()}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Habilitar CORS para todas as rotas
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar detector de spam
detector = SpamDetector(
    model_path='spam_model.pkl',
    vectorizer_path='vectorizer.pkl'
)


@app.route('/health', methods=['GET'])
def health():
    """Verificar saúde da API"""
    return jsonify({'status': 'ok', 'message': 'API está funcionando'}), 200


# Create tables if they don't exist (run at startup)
with app.app_context():
    db.create_all()


@app.route('/predict', methods=['POST'])
def predict():
    """
    Classificar uma mensagem como spam ou ham
    
    Esperado: {"text": "sua mensagem aqui"}
    Retorna: {"label": "spam/ham", "confidence": float}
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Campo "text" é obrigatório'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'Texto inválido'}), 400
        
        result = detector.predict(text)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao processar predição', 'details': str(e)}), 500


@app.route('/predict-explain', methods=['POST'])
def predict_explain():
    """
    Classificar uma mensagem com explicação detalhada
    
    Esperado: {"text": "sua mensagem aqui"}
    Retorna: Predição com explicação, top features, e confiança normalizada
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Campo "text" é obrigatório'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'Texto inválido'}), 400
        
        result = detector.predict_with_explanation(text)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao processar predição', 'details': str(e)}), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    """Retornar métricas do modelo treinado"""
    try:
        metrics = detector.get_metrics()
        
        if not metrics:
            return jsonify({'error': 'Modelo não foi treinado ainda'}), 400
        
        return jsonify({
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1'],
            'confusion_matrix': metrics['confusion_matrix'],
            'classification_report': metrics['classification_report']
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Erro ao obter métricas', 'details': str(e)}), 500


@app.route('/train', methods=['POST'])
def train():
    """
    Treinar o modelo com dados de um CSV
    
    Esperado: {"csv_path": "caminho/para/arquivo.csv"}
    """
    try:
        data = request.get_json()
        
        if not data or 'csv_path' not in data:
            return jsonify({'error': 'Campo "csv_path" é obrigatório'}), 400
        
        csv_path = data['csv_path']
        
        if not os.path.exists(csv_path):
            return jsonify({'error': f'Arquivo não encontrado: {csv_path}'}), 400
        
        # Carregar dados
        X, y = detector.load_data(csv_path)
        
        # Treinar modelo
        X_test, y_test, y_pred = detector.train(X, y)
        
        # Salvar modelo
        detector.save_model()
        
        metrics = detector.get_metrics()
        
        return jsonify({
            'message': 'Modelo treinado com sucesso',
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1']
        }), 200
    
    except FileNotFoundError as e:
        return jsonify({'error': f'Arquivo não encontrado: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao treinar modelo', 'details': str(e)}), 500


@app.route('/send', methods=['POST'])
def send_message():
    """
    Verifica se é spam e envia a mensagem se permitido.
    
    Esperado: {"message": "sua mensagem aqui", "recipient": "email@example.com"}
    Retorna: 
      - Se spam: {"status": "blocked", "reason": "Mensagem identificada como spam"}
      - Se ham: {"status": "sent", "message_id": "...", "recipient": "..."}
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
        result = detector.predict(message)
        
        # Se for spam, bloquear
        if result['label'] == 'spam':
            return jsonify({
                'status': 'blocked',
                'reason': 'Mensagem identificada como spam',
                'confidence': result['confidence'],
                'message': message[:100] + '...' if len(message) > 100 else message
            }), 403
        
        # Se for ham, simular envio
        # Optionally persist the sent message in the database
        try:
            with app.app_context():
                rec = EmailRecord(
                    sender='me@example.com',
                    recipient=recipient,
                    subject=('(sent) ' + message[:60]) if message else '(sent)',
                    body=message,
                    received=datetime.now(),
                    is_spam=(result['label'] == 'spam'),
                    spam_score=result.get('confidence', 0.0)
                )
                db.session.add(rec)
                db.session.commit()
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


@app.route('/info', methods=['GET'])
def info():
    """Informações sobre a API"""
    is_model_loaded = detector.model is not None and detector.vectorizer is not None
    
    return jsonify({
        'name': 'Spam Detector API',
        'version': '1.1.0',
        'model_status': 'carregado' if is_model_loaded else 'não carregado',
        'endpoints': {
            'GET /health': 'Verificar saúde da API',
            'POST /predict': 'Classificar mensagem (body: {"text": "..."})',
            'POST /predict-explain': 'Classificar com explicação detalhada ⭐ NOVO',
            'POST /send': 'Enviar mensagem com verificação de spam',
            'GET /metrics': 'Obter métricas do modelo',
            'POST /train': 'Treinar modelo (body: {"csv_path": "..."})',
            'GET /info': 'Informações sobre a API'
        }
    }), 200


@app.route('/emails', methods=['GET'])
def list_emails():
    """List all stored emails"""
    try:
        with app.app_context():
            records = EmailRecord.query.order_by(EmailRecord.received.desc()).all()
            return jsonify([r.to_dict() for r in records]), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao listar emails', 'details': str(e)}), 500


@app.route('/emails', methods=['POST'])
def create_email():
    """Create/store an email record

    Esperado: { sender, recipient, subject, body, received (iso)?, is_spam (bool), spam_score (float) }
    """
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

        with app.app_context():
            rec = EmailRecord(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
                received=received_dt,
                is_spam=is_spam,
                spam_score=spam_score
            )
            db.session.add(rec)
            db.session.commit()
            return jsonify(rec.to_dict()), 201

    except Exception as e:
        return jsonify({'error': 'Erro ao criar email', 'details': str(e)}), 500


if __name__ == '__main__':
    # Verificar se modelo está carregado
    if detector.model is None or detector.vectorizer is None:
        print("⚠️  ATENÇÃO: Modelo não foi encontrado!")
        print("Execute primeiro: python pretrained_model.py")
        print("Ou treine seu próprio modelo com: python train.py")
    else:
        print("✓ Modelo carregado com sucesso!")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

