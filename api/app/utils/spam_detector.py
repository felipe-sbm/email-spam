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
        
        # Obter feature names
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Obter coeficientes do modelo (pesos das palavras)
        # Para kernel linear, coef_ é acessível
        if self.model.kernel == 'linear':
            coefs = self.model.coef_.toarray()[0]
            
            # Encontrar palavras na mensagem que contribuíram para a decisão
            # Primeiro, pegar índices não-zero do vetor da mensagem
            msg_vector = X_tfidf.toarray()[0]
            word_indices = msg_vector.nonzero()[0]
            
            explanation = []
            for idx in word_indices:
                word = feature_names[idx]
                weight = coefs[idx]
                # TF-IDF score da palavra na mensagem
                tfidf_score = msg_vector[idx]
                # Contribuição = peso * tfidf
                contribution = weight * tfidf_score
                
                explanation.append({
                    'word': word,
                    'weight': float(weight),
                    'contribution': float(contribution)
                })
            
            # Ordenar por contribuição (absoluta ou sinalizada dependendo do interesse)
            # Spam geralmente tem contribuição positiva alta
            explanation.sort(key=lambda x: x['contribution'], reverse=True)
            
            return {
                'text': text,
                'label': prediction,
                'confidence': prob,
                'explanation': explanation[:10]  # Top 10 palavras influentes
            }
        
        return {
            'text': text,
            'label': prediction,
            'confidence': prob,
            'explanation': "Explicação disponível apenas para kernel linear"
        }

    def save_model(self):
        """Salva o modelo e vetorizador em disco"""
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"Modelo salvo em {self.model_path} e {self.vectorizer_path}")

    def load_model(self):
        """Carrega o modelo e vetorizador do disco"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.model = None
            self.vectorizer = None

    def get_metrics(self):
        """Retorna as métricas do último treinamento"""
        return self.metrics
