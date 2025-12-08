# 📊 Arquitetura da API de Spam Detection

## Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE/USUARIO                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ POST /send
                     │ {"message": "...", "recipient": "..."}
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   API FLASK (app.py)                        │
│                                                              │
│  Recebe mensagem do cliente                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           SPAM DETECTOR (spam_detector.py)                  │
│                                                              │
│  1. Vetoriza texto com TF-IDF                              │
│  2. Passa para modelo SVM                                   │
│  3. Retorna predição + confiança                            │
└─────────────┬──────────────────────┬────────────────────────┘
              │                      │
      ┌───────▼────────┐    ┌────────▼─────────┐
      │   SPAM (❌)    │    │  HAM/LEGIT (✅)  │
      │                │    │                  │
      │ Bloqueia       │    │ Permite envio    │
      │ Retorna 403    │    │ Retorna 200      │
      └────────────────┘    └──────────────────┘


## Arquivos do Projeto

📁 api/
├── app.py ............................ API Flask com endpoints
├── spam_detector.py .................. Classe principal de detecção
├── pretrained_model.py ............... Gera modelo pré-treinado (usar 1x)
├── train.py .......................... Treina com dados customizados
├── test_api.py ....................... Tester automático de endpoints
├── requirements.txt .................. Dependências
├── README.md ......................... Documentação completa
├── QUICKSTART.md ..................... Guia rápido (esse arquivo)
├── spam_model.pkl .................... Modelo IA (gerado automaticamente)
└── vectorizer.pkl .................... Vetorizador (gerado automaticamente)


## Setup Visual

┌──────────────┐
│ pip install  │  Instala Flask, scikit-learn, pandas, requests
│ requirements │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ python               │  Gera spam_model.pkl + vectorizer.pkl
│ pretrained_model.py  │  (Execute UMA VEZ)
└──────┬───────────────┘
       │
       ▼
┌──────────────────┐
│ python app.py    │  API rodando em http://localhost:5000
└──────────────────┘


## Endpoints

GET /health
├─ Status: 200
└─ Retorna: {"status": "ok"}

GET /info
├─ Status: 200
└─ Retorna: Documentação de endpoints

POST /predict
├─ Input: {"text": "mensagem"}
├─ Status: 200
└─ Retorna: {"label": "spam/ham", "confidence": float}

POST /send ⭐ PRINCIPAL
├─ Input: {"message": "...", "recipient": "..."}
├─ Se SPAM:
│  ├─ Status: 403
│  └─ Retorna: {"status": "blocked", "reason": "..."}
└─ Se HAM:
   ├─ Status: 200
   └─ Retorna: {"status": "sent", "message_id": "...", ...}

GET /metrics
├─ Status: 200
└─ Retorna: Acurácia, Precisão, Recall, F1-Score


## Modelo IA (SVM + TF-IDF)

Treinamento:
  Texto → TF-IDF Vetorization → SVM Classification → Predição

Exemplo:
  "Click here to win $1000!"
         ↓
  Vetorizado com TF-IDF
         ↓
  Passa pelo SVM
         ↓
  Resultado: SPAM (confiança: 2.34)


## Fluxo Completo de Envio

USUÁRIO ENVIA MENSAGEM
        ↓
API RECEBE (/send)
        ↓
SPAM_DETECTOR.PREDICT()
        ↓
┌───────┴────────┐
│                │
▼ (spam)         ▼ (ham)
BLOQUEIA         ENVIA
❌ 403           ✅ 200
```

## Como Usar em Seu Código

```python
# 1. Fazer predição de texto
POST /predict
Input: {"text": "sua mensagem"}
Output: {"label": "spam/ham", "confidence": float}

# 2. Enviar mensagem com verificação
POST /send
Input: {"message": "sua mensagem", "recipient": "email@example.com"}
Output: {"status": "sent"} ou {"status": "blocked"}

# 3. Ver performance do modelo
GET /metrics
Output: Acurácia, Precisão, Recall, F1-Score...
```

---

**Pronto para usar!** 🚀
