#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar os endpoints da API localmente.
Útil para testar sem precisar fazer curl manual.
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_health():
    """Testar saúde da API"""
    print("\n🔍 Testando /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_info():
    """Obter informações da API"""
    print("\n🔍 Testando /info...")
    try:
        response = requests.get(f"{BASE_URL}/info")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_predict():
    """Testar classificação de mensagens"""
    print("\n🔍 Testando /predict...")
    
    test_cases = [
        {"text": "Click here to win $1000!", "expected": "spam"},
        {"text": "Hi, how are you?", "expected": "ham"},
        {"text": "Limited time offer, buy now!", "expected": "spam"},
        {"text": "Let's meet tomorrow at 3pm", "expected": "ham"},
    ]
    
    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json={"text": test["text"]}
            )
            result = response.json()
            label = result.get('label')
            emoji = "✓" if label == test['expected'] else "❌"
            print(f"{emoji} '{test['text'][:40]}...' -> {label}")
        except Exception as e:
            print(f"❌ Erro: {e}")

def test_send():
    """Testar envio de mensagens (com verificação de spam)"""
    print("\n🔍 Testando /send...")
    
    test_cases = [
        {
            "message": "Work from home and earn money!",
            "recipient": "user@example.com",
            "expected_status": "blocked"
        },
        {
            "message": "Meeting confirmed for tomorrow",
            "recipient": "user@example.com",
            "expected_status": "sent"
        },
    ]
    
    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/send",
                json={
                    "message": test["message"],
                    "recipient": test["recipient"]
                }
            )
            result = response.json()
            status = result.get('status')
            emoji = "✓" if status == test['expected_status'] else "❌"
            print(f"{emoji} '{test['message'][:40]}...' -> {status}")
            
            if status == "blocked":
                print(f"   Razão: {result.get('reason')}")
            else:
                print(f"   Enviado para: {result.get('recipient')}")
        except Exception as e:
            print(f"❌ Erro: {e}")

def main():
    print("=" * 60)
    print("🧪 Testador de API - Spam Detector")
    print("=" * 60)
    print("Certificado de que a API está rodando em http://localhost:5000")
    
    try:
        test_health()
        test_info()
        test_predict()
        test_send()
        
        print("\n" + "=" * 60)
        print("✓ Todos os testes concluídos!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API em http://localhost:5000")
        print("Certifique-se de que a API está rodando: python app.py")

if __name__ == '__main__':
    main()
