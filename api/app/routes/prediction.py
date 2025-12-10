from flask import Blueprint, request, jsonify
from app.services import spam_service
import os

bp = Blueprint('prediction', __name__)

@bp.route('/health', methods=['GET'])
def health():
    """Verificar saúde da API"""
    return jsonify({'status': 'ok', 'message': 'API está funcionando'}), 200

@bp.route('/predict', methods=['POST'])
def predict():
    """
    Classificar uma mensagem como spam ou ham
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Campo "text" é obrigatório'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'Texto inválido'}), 400
        
        result = spam_service.predict(text)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao processar predição', 'details': str(e)}), 500

@bp.route('/predict-explain', methods=['POST'])
def predict_explain():
    """
    Classificar uma mensagem com explicação detalhada
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Campo "text" é obrigatório'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'Texto inválido'}), 400
        
        result = spam_service.predict_with_explanation(text)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro ao processar predição', 'details': str(e)}), 500

@bp.route('/metrics', methods=['GET'])
def metrics():
    """Retornar métricas do modelo treinado"""
    try:
        metrics = spam_service.get_metrics()
        
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

@bp.route('/train', methods=['POST'])
def train():
    """
    Treinar o modelo com dados de um CSV
    """
    try:
        data = request.get_json()
        
        if not data or 'csv_path' not in data:
            return jsonify({'error': 'Campo "csv_path" é obrigatório'}), 400
        
        csv_path = data['csv_path']
        
        if not os.path.exists(csv_path):
            return jsonify({'error': f'Arquivo não encontrado: {csv_path}'}), 400
        
        # Carregar dados
        X, y = spam_service.load_data(csv_path)
        
        # Treinar modelo
        spam_service.train(X, y)
        
        # Salvar modelo
        spam_service.save_model()
        
        metrics = spam_service.get_metrics()
        
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

@bp.route('/info', methods=['GET'])
def info():
    """Informações sobre a API"""
    is_loaded = spam_service.is_model_loaded()
    
    return jsonify({
        'name': 'Spam Detector API',
        'version': '1.1.0',
        'model_status': 'carregado' if is_loaded else 'não carregado',
        'endpoints': {
            'GET /health': 'Verificar saúde da API',
            'POST /predict': 'Classificar mensagem (body: {"text": "..."})',
            'POST /predict-explain': 'Classificar com explicação detalhada',
            'POST /send': 'Enviar mensagem com verificação de spam',
            'GET /metrics': 'Obter métricas do modelo',
            'POST /train': 'Treinar modelo (body: {"csv_path": "..."})',
            'GET /info': 'Informações sobre a API'
        }
    }), 200
