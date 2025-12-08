# -*- coding: utf-8 -*-
"""
Script para gerar um modelo pré-treinado usando um dataset público de spam.
Execute este script UMA VEZ para gerar spam_model.pkl e vectorizer.pkl
"""

import pickle
import os
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd


def download_and_train():
    """
    Baixa um dataset de spam público e treina o modelo.
    Este é um exemplo usando dados inline para demonstração.
    """
    
    print("Gerando modelo pré-treinado de spam detection...")
    
    # Dataset de exemplo com mensagens comuns de spam
    spam_data = [
        # SPAM
        ("Click here to win $1000!", "spam"),
        ("Congratulations! You have won!", "spam"),
        ("Limited time offer! Buy now!", "spam"),
        ("Free money! Get rich quick!", "spam"),
        ("Verify your account by clicking here", "spam"),
        ("You have been selected as winner", "spam"),
        ("Act now or lose this chance", "spam"),
        ("Enlarge your body naturally", "spam"),
        ("Work from home and earn money", "spam"),
        ("Call now for free consultation", "spam"),
        ("Unbeatable prices just for you", "spam"),
        ("Double your income now", "spam"),
        ("Join our exclusive club today", "spam"),
        ("Weight loss in just 2 weeks", "spam"),
        ("Transform your life overnight", "spam"),
        ("Apply for credit card instantly", "spam"),
        ("Meet singles in your area", "spam"),
        ("Your prize is waiting", "spam"),
        ("Don't miss this opportunity", "spam"),
        ("Get approval for $50000 loan", "spam"),
        
        # HAM
        ("Hey, how are you doing?", "ham"),
        ("Can we schedule a meeting tomorrow?", "ham"),
        ("The project is on track", "ham"),
        ("Thank you for your help", "ham"),
        ("I will send you the files", "ham"),
        ("Good morning, how was your day?", "ham"),
        ("Let's catch up this weekend", "ham"),
        ("The presentation is ready", "ham"),
        ("I got your message", "ham"),
        ("Thanks for the update", "ham"),
        ("See you at the office", "ham"),
        ("The report is attached", "ham"),
        ("Let me know what you think", "ham"),
        ("Hope you are well", "ham"),
        ("Check the calendar for availability", "ham"),
        ("That sounds great", "ham"),
        ("I agree with your idea", "ham"),
        ("The deadline is next Friday", "ham"),
        ("Looking forward to the meeting", "ham"),
        ("Everything looks good", "ham"),
    ]
    
    df = pd.DataFrame(spam_data, columns=['text', 'label'])
    
    print(f"Dataset com {len(df)} mensagens carregado")
    print(f"Spam: {len(df[df['label'] == 'spam'])} | Ham: {len(df[df['label'] == 'ham'])}")
    
    # Vetorização
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X_tfidf = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Divisão treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y, test_size=0.2, random_state=42
    )
    
    # Treinamento
    print("\nTreinando modelo SVM...")
    model = SVC(kernel='linear', C=1.0, random_state=42, probability=True)
    model.fit(X_train, y_train)
    
    # Avaliação
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label='spam', zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label='spam', zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label='spam', zero_division=0)
    
    print(f"Acurácia: {accuracy:.4f}")
    print(f"Precisão: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Salvar modelo
    print("\nSalvando modelo...")
    pickle.dump(model, open('spam_model.pkl', 'wb'))
    pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
    
    print("✓ Modelo pré-treinado salvo com sucesso!")
    print("  - spam_model.pkl")
    print("  - vectorizer.pkl")
    print("\nAgora você pode usar a API sem precisar treinar novamente!")


if __name__ == '__main__':
    download_and_train()
