import pickle
import os
import math
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class SpamDetector:
    """Classe para detectar spam em mensagens usando SVM"""
    
    def __init__(self, model_path='spam_model.pkl', vectorizer_path='vectorizer.pkl'):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.metrics = {}
        
        # Carregar modelo e vetorizador se existirem
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            self.load_model()
    
    def load_data(self, csv_path):
        """Carrega dados do CSV"""
        df = pd.read_csv(csv_path)
        X = df['text']
        y = df['label']
        return X, y
    
    def train(self, X, y, test_size=0.3, random_state=42):
        """Treina o modelo SVM com TF-IDF"""
        # Vetorizar
        self.vectorizer = TfidfVectorizer()
        X_tfidf = self.vectorizer.fit_transform(X)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X_tfidf, y, test_size=test_size, random_state=random_state
        )
        
        # Treinar modelo
        self.model = SVC(kernel='linear', C=1.0, random_state=random_state)
        self.model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = self.model.predict(X_test)
        self._calculate_metrics(y_test, y_pred)
        
        print("Modelo SVM treinado com sucesso!")
        print(f"Acurácia: {self.metrics['accuracy']:.4f}")
        
        return X_test, y_test, y_pred
    
    def _calculate_metrics(self, y_test, y_pred):
        """Calcula métricas do modelo"""
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, pos_label='spam', zero_division=0),
            'recall': recall_score(y_test, y_pred, pos_label='spam', zero_division=0),
            'f1': f1_score(y_test, y_pred, pos_label='spam', zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred)
        }
    
    def predict(self, text):
        """Prediz se uma mensagem é spam"""
        if self.model is None or self.vectorizer is None:
            raise ValueError("Modelo não carregado. Treine o modelo primeiro.")
        
        X_tfidf = self.vectorizer.transform([text])
        prediction = self.model.predict(X_tfidf)[0]
        # `decision_function` retorna a distância ao hiperplano (pode ser negativa).
        # Normalizamos este valor usando uma sigmoide para mapear para [0, 1]
        # e retornar uma 'confidence' compreensível como probabilidade.
        raw_conf = float(self.model.decision_function(X_tfidf)[0])
        prob = 1.0 / (1.0 + math.exp(-raw_conf))

        return {
            'text': text,
            'label': prediction,
            'confidence': float(prob)
        }
    
    def predict_with_explanation(self, text):
        """
        Prediz e retorna explicação detalhada sobre por que é spam ou não
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Modelo não carregado. Treine o modelo primeiro.")
        
        # Fazer predição
        X_tfidf = self.vectorizer.transform([text])
        prediction = self.model.predict(X_tfidf)[0]
        confidence = self.model.decision_function(X_tfidf)[0]
        
        # Normalizar confiança: mapear o valor bruto (distance) para probabilidade [0-1]
        raw_conf = float(confidence)
        prob = 1.0 / (1.0 + math.exp(-raw_conf))
        normalized_confidence = min(max(prob * 100.0, 0.0), 100.0)
        
        # Extrair features mais importantes
        feature_names = self.vectorizer.get_feature_names_out()
        feature_scores = X_tfidf.toarray()[0]
        
        # Encontrar os top 5 features mais importantes
        top_indices = (-feature_scores).argsort()[:5]
        top_features = []
        
        for idx in top_indices:
            if feature_scores[idx] > 0:
                top_features.append({
                    'word': feature_names[idx],
                    'score': float(feature_scores[idx]),
                    'is_spam_indicator': self._is_spam_word(feature_names[idx])
                })
        
        return {
            'text': text,
            'label': prediction,
            'raw_confidence': raw_conf,
            'confidence': float(prob),
            'normalized_confidence': normalized_confidence,
            'is_spam': prediction == 'spam',
            'explanation': self._generate_explanation(prediction, top_features, text),
            'top_features': top_features,
            'token_count': len(text.split()),
            'message_length': len(text),
            'model_version': '1.0.0'
        }
    
    def _is_spam_word(self, word):
        """Verifica se uma palavra é comumente associada com spam"""
        spam_keywords = {
            'click', 'win', 'free', 'limited', 'offer', 'now', 'money', 'earn',
            'cash', 'urgent', 'act', 'verify', 'confirm', 'congratulations',
            'winner', 'prize', 'buy', 'order', 'discount', 'sale'
        }
        return word.lower() in spam_keywords
    
    def _generate_explanation(self, label, features, text):
        """Gera explicação em linguagem natural"""
        if label == 'spam':
            if features:
                feature_list = ', '.join([f'"{f["word"]}"' for f in features[:3]])
                return f"Mensagem classificada como SPAM. Palavras-chave detectadas: {feature_list}. O modelo identificou padrões típicos de mensagens de spam."
            else:
                return "Mensagem classificada como SPAM baseado na análise do modelo."
        else:
            return "Mensagem classificada como LEGÍTIMA. O texto não apresenta características típicas de spam."
    
    def save_model(self):
        """Salva o modelo e vetorizador"""
        pickle.dump(self.model, open(self.model_path, 'wb'))
        pickle.dump(self.vectorizer, open(self.vectorizer_path, 'wb'))
        print(f"Modelo salvo em {self.model_path} e {self.vectorizer_path}")
    
    def load_model(self):
        """Carrega o modelo e vetorizador salvos"""
        self.model = pickle.load(open(self.model_path, 'rb'))
        self.vectorizer = pickle.load(open(self.vectorizer_path, 'rb'))
        print("Modelo carregado com sucesso!")
    
    def get_metrics(self):
        """Retorna as métricas do modelo"""
        return self.metrics