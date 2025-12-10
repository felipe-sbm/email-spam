from flask import current_app
from app.utils.spam_detector import SpamDetector

_detector = None

def get_detector():
    global _detector
    if _detector is None:
        _detector = SpamDetector(
            model_path=current_app.config['MODEL_PATH'],
            vectorizer_path=current_app.config['VECTORIZER_PATH']
        )
    return _detector

def predict(text):
    return get_detector().predict(text)

def predict_with_explanation(text):
    return get_detector().predict_with_explanation(text)

def load_data(csv_path):
    return get_detector().load_data(csv_path)

def train(X, y):
    return get_detector().train(X, y)

def save_model():
    get_detector().save_model()

def get_metrics():
    return get_detector().get_metrics()

def is_model_loaded():
    det = get_detector()
    return det.model is not None and det.vectorizer is not None
