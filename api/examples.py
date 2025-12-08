#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplos práticos de uso da API Spam Detector

Este arquivo demonstra como usar a API em diferentes cenários.
"""

import requests
import json

BASE_URL = "http://localhost:5000"


class SpamDetectorClient:
    """Cliente para interagir com a API de Spam Detection"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def predict(self, text):
        """Apenas classifica a mensagem (sem enviar)"""
        response = requests.post(
            f"{self.base_url}/predict",
            json={"text": text}
        )
        return response.json() if response.status_code == 200 else None
    
    def send_message(self, message, recipient):
        """Envia mensagem se não for spam, senão bloqueia"""
        response = requests.post(
            f"{self.base_url}/send",
            json={"message": message, "recipient": recipient}
        )
        return response.status_code, response.json()
    
    def get_metrics(self):
        """Obter métricas do modelo"""
        response = requests.get(f"{self.base_url}/metrics")
        return response.json() if response.status_code == 200 else None


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

def exemplo_1_classificacao_simples():
    """Exemplo 1: Apenas classificar mensagens"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Classificação Simples")
    print("="*70)
    
    client = SpamDetectorClient()
    
    mensagens = [
        "Click here to win $1000!",
        "Hi, how are you doing?",
        "Limited time offer - buy now!",
        "Let's schedule a meeting for tomorrow",
        "Congratulations! You have won!",
        "Thank you for your message",
    ]
    
    print("\nClassificando mensagens...\n")
    for mensagem in mensagens:
        result = client.predict(mensagem)
        emoji = "🚨" if result['label'] == 'spam' else "✓"
        print(f"{emoji} {mensagem[:40]:.<40} -> {result['label'].upper()}")


def exemplo_2_envio_com_bloqueio():
    """Exemplo 2: Enviar mensagens (bloqueadas se spam)"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Envio com Bloqueio Automático")
    print("="*70)
    
    client = SpamDetectorClient()
    
    casos_teste = [
        {
            "message": "Hi friend! How are you?",
            "recipient": "friend@example.com",
            "descricao": "Mensagem legítima"
        },
        {
            "message": "Work from home and earn $5000/month!",
            "recipient": "spam@example.com",
            "descricao": "Mensagem com spam"
        },
        {
            "message": "The project is complete. Check attachment.",
            "recipient": "boss@example.com",
            "descricao": "Email profissional"
        },
        {
            "message": "CLICK HERE NOW! Limited time!",
            "recipient": "suspicious@example.com",
            "descricao": "Mensagem suspeita"
        },
    ]
    
    print("\nEnviando mensagens...\n")
    for caso in casos_teste:
        status_code, result = client.send_message(
            caso['message'],
            caso['recipient']
        )
        
        if status_code == 200:
            print(f"✅ ENVIADA: {caso['descricao']}")
            print(f"   Para: {result['recipient']}")
            print(f"   ID: {result['message_id']}\n")
        else:
            print(f"❌ BLOQUEADA: {caso['descricao']}")
            print(f"   Motivo: {result['reason']}")
            print(f"   Confiança: {result['confidence']:.2f}\n")


def exemplo_3_analise_desempenho():
    """Exemplo 3: Analisar métricas do modelo"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Métricas de Desempenho do Modelo")
    print("="*70)
    
    client = SpamDetectorClient()
    metrics = client.get_metrics()
    
    if metrics:
        print(f"\n📊 Desempenho do Modelo SVM:")
        print(f"   Acurácia:  {metrics['accuracy']:.2%}")
        print(f"   Precisão:  {metrics['precision']:.2%}")
        print(f"   Recall:    {metrics['recall']:.2%}")
        print(f"   F1-Score:  {metrics['f1_score']:.2%}")
        print(f"\nMatriz de Confusão:")
        cm = metrics['confusion_matrix']
        print(f"   TP: {cm[0][0]}, FP: {cm[0][1]}")
        print(f"   FN: {cm[1][0]}, TN: {cm[1][1]}")
    else:
        print("❌ Não foi possível obter métricas")


def exemplo_4_detector_de_email():
    """Exemplo 4: Detector de email completo"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Detector de Email em Produção")
    print("="*70)
    
    client = SpamDetectorClient()
    
    # Simular uma caixa de entrada
    inbox = [
        {"from": "boss@company.com", "subject": "Project Update", 
         "body": "Can you send me the quarterly report?"},
        {"from": "noreply@deals.com", "subject": "GET 50% OFF NOW!",
         "body": "Click here to claim your discount before it expires!"},
        {"from": "friend@email.com", "subject": "Coffee Tomorrow?",
         "body": "Are you free tomorrow at 3pm for coffee?"},
        {"from": "banking@scam.com", "subject": "URGENT: Verify Account",
         "body": "Your account has been compromised. Click here to verify."},
    ]
    
    print("\nFiltrando emails da caixa de entrada...\n")
    
    spam_count = 0
    ham_count = 0
    
    for email in inbox:
        status_code, result = client.send_message(
            email['body'],
            email['from']
        )
        
        if status_code == 200:
            print(f"{email['from']:30} -> {email['subject']}")
            ham_count += 1
        else:
            print(f"{email['from']:30} -> {email['subject']} [SPAM]")
            spam_count += 1
    
    print(f"\n📈 Resumo:")
    print(f"   Emails legítimos: {ham_count}")
    print(f"   Emails spam:      {spam_count}")
    print(f"   Taxa de filtro:   {spam_count/len(inbox):.0%}")


def exemplo_5_batch_processing():
    """Exemplo 5: Processar múltiplas mensagens em lote"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Processamento em Lote")
    print("="*70)
    
    client = SpamDetectorClient()
    
    # Lista de mensagens para processar
    mensagens = [
        ("msg_001", "Nice meeting with you today", "friend@email.com"),
        ("msg_002", "Win $1 Million now!", "lottery@spam.com"),
        ("msg_003", "Project deadline extended to next week", "work@company.com"),
        ("msg_004", "Limited offer expires today", "sales@shop.com"),
        ("msg_005", "How about lunch tomorrow?", "colleague@work.com"),
    ]
    
    print("\nProcessando lote de mensagens...\n")
    
    resultados = {
        "enviadas": [],
        "bloqueadas": []
    }
    
    for msg_id, message, recipient in mensagens:
        status_code, result = client.send_message(message, recipient)
        
        if status_code == 200:
            resultados["enviadas"].append({
                "id": msg_id,
                "to": recipient,
                "message_id": result['message_id']
            })
        else:
            resultados["bloqueadas"].append({
                "id": msg_id,
                "reason": result['reason'],
                "confidence": result['confidence']
            })
    
    print(f"📤 Enviadas: {len(resultados['enviadas'])}")
    for item in resultados["enviadas"]:
        print(f"   {item['id']}: {item['to']}")
    
    print(f"\n🚫 Bloqueadas: {len(resultados['bloqueadas'])}")
    for item in resultados["bloqueadas"]:
        print(f"   {item['id']}: {item['reason']}")


def exemplo_6_api_rest_com_curl():
    """Exemplo 6: Usar a API com curl (terminal)"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Usando curl no Terminal")
    print("="*70)
    
    print("""
Classificar uma mensagem:
$ curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Click here to win money!"}'

Enviar mensagem (com bloqueio de spam):
$ curl -X POST http://localhost:5000/send \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hi how are you?", "recipient": "user@example.com"}'

Obter métricas:
$ curl http://localhost:5000/metrics

Verificar saúde da API:
$ curl http://localhost:5000/health
    """)


# ============================================================================
# EXECUTAR EXEMPLOS
# ============================================================================

if __name__ == '__main__':
    print("\n" + "🧪 EXEMPLOS DE USO - SPAM DETECTOR API".center(70))
    print("Certifique-se de que a API está rodando: python app.py".center(70))
    
    try:
        # Executar exemplos
        exemplo_1_classificacao_simples()
        exemplo_2_envio_com_bloqueio()
        exemplo_3_analise_desempenho()
        exemplo_4_detector_de_email()
        exemplo_5_batch_processing()
        exemplo_6_api_rest_com_curl()
        
        print("\n" + "="*70)
        print("✓ Todos os exemplos executados com sucesso!".center(70))
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print(ValueError("\nErro: Não foi possível conectar à API"))
        print(ValueError("Certifique-se de que está rodando: python app.py\n"))
    except Exception as e:
        print(f"\nErro: {e}\n")
