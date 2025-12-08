# ✨ RESUMO: API de Spam Detection - Pronta para Usar

## 🎯 O que foi criado?

Uma **API Flask completa** que:
- ✅ Recebe mensagens via HTTP
- ✅ Verifica automaticamente se é spam
- ✅ **Bloqueia mensagens spam** (retorna erro 403)
- ✅ **Envia apenas mensagens legítimas** (retorna sucesso 200)
- ✅ Usa **modelo pré-treinado** (não precisa treinar toda vez)
- ✅ Pode ser integrada em qualquer projeto

---

## 📁 Arquivos Criados/Modificados

```
api/
├── 🔧 CONFIGURAÇÃO
│   ├── requirements.txt ..................... Dependências (pip install)
│   ├── .gitignore ........................... Ignora arquivos grandes
│   └── pretrained_model.py .................. Gera modelo pré-treinado (1x)
│
├── 💻 CÓDIGO PRINCIPAL
│   ├── app.py .............................. API Flask com todos endpoints
│   ├── spam_detector.py ..................... Classe de detecção de spam
│   └── train.py ............................ Treina com dados customizados
│
├── 🧪 TESTES & EXEMPLOS
│   ├── test_api.py .......................... Tester automático
│   ├── examples.py .......................... 6 exemplos práticos
│   └── QUICKSTART.md ........................ Guia rápido (5 min)
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md ........................... Documentação completa
│   ├── ARCHITECTURE.md ..................... Diagramas de arquitetura
│   └── SETUP.md (este arquivo) ............. Resumo final
│
└── 🤖 MODELOS (gerados automaticamente)
    ├── spam_model.pkl ....................... Modelo SVM
    └── vectorizer.pkl ....................... Vetorizador TF-IDF
```

---

## 🚀 Como Usar (3 passos)

### 1️⃣ Instalar
```bash
pip install -r requirements.txt
```

### 2️⃣ Gerar modelo pré-treinado (execute UMA VEZ)
```bash
python pretrained_model.py
```

### 3️⃣ Iniciar API
```bash
python app.py
```

API disponível em: **http://localhost:5000** ✨

---

## 📡 Endpoints Principais

### **POST /send** ⭐ (Главный endpoint)
Envia mensagem se legítima, bloqueia se spam

```bash
# Mensagem legítima (será enviada)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!", "recipient": "user@example.com"}'

# Resposta (sucesso):
{
  "status": "sent",
  "message_id": "msg_a1b2c3d4",
  "recipient": "user@example.com",
  "timestamp": "2025-12-03T..."
}
```

```bash
# Mensagem spam (será bloqueada)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Click to win $1000!", "recipient": "...@gmail.com"}'

# Resposta (bloqueado):
{
  "status": "blocked",
  "reason": "Mensagem identificada como spam",
  "confidence": 2.34
}
```

### **POST /predict**
Apenas classifica (sem enviar)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "sua mensagem"}'
```

### **GET /metrics**
Métricas do modelo

```bash
curl http://localhost:5000/metrics
```

### **GET /health**
Verificar se API está rodando

```bash
curl http://localhost:5000/health
```

---

## 💻 Usar em Python

```python
import requests

# Enviar mensagem
response = requests.post(
    'http://localhost:5000/send',
    json={
        'message': 'Oi, tudo bem?',
        'recipient': 'amigo@example.com'
    }
)

if response.status_code == 200:
    print("✓ Enviado:", response.json()['message_id'])
else:
    print("❌ Bloqueado:", response.json()['reason'])
```

---

## 🧪 Testar

### Testar tudo automaticamente:
```bash
python test_api.py
```

### Ver exemplos práticos:
```bash
python examples.py
```

---

## 🎓 Tecnologias Usadas

- **Framework**: Flask (API REST)
- **ML**: scikit-learn (SVM + TF-IDF)
- **Vetorização**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Algoritmo**: Support Vector Machine (SVM) com kernel linear
- **Serialização**: Pickle (salvar/carregar modelos)

---

## 📊 Como Funciona

```
Mensagem do Usuário
        ↓
TF-IDF Vetorização (converte texto em números)
        ↓
Modelo SVM (classifica baseado em padrões)
        ↓
Predição: SPAM ou HAM
        ↓
├─ Se SPAM → Retorna 403 (Bloqueado)
└─ Se HAM → Retorna 200 (Enviado)
```

---

## 📈 Performance

Métricas esperadas (depende do dataset):
- **Acurácia**: ~95% (quão correto é o modelo)
- **Precisão**: ~92% (dos detectados spam, quantos são reais)
- **Recall**: ~98% (consegue pegar mais spams)
- **F1-Score**: ~95% (média ponderada)

Veja com: `curl http://localhost:5000/metrics`

---

## ⚙️ Customização

### Treinar com seus dados:
```bash
python train.py
# (escolha um arquivo CSV com colunas: text, label)
# Depois reinicie a API
```

### Formato do CSV:
```
text,label
"Click here to win",spam
"Hi how are you",ham
```

---

## 🔒 Segurança

- Validação de entrada (não aceita texto vazio)
- Tratamento de erros (try/except)
- Headers CORS podem ser adicionados conforme necessário

---

## 📝 Próximos Passos

1. ✅ API funcionando localmente
2. 🔜 Deploy em produção (Heroku, AWS, etc)
3. 🔜 Integração com banco de dados
4. 🔜 Interface web (Blazor/React)
5. 🔜 Melhorar modelo com mais dados

---

## ❓ FAQ

**P: Preciso treinar toda vez que abro?**
A: Não! Os arquivos `.pkl` são salvos automaticamente.

**P: Posso usar com dados em português?**
A: Sim! O modelo funciona com qualquer idioma.

**P: Como adiciono meu próprio dataset?**
A: Execute `python train.py` e escolha seu arquivo CSV.

**P: A API pode rodar em produção?**
A: Sim! Use Gunicorn ou similar em vez de debug mode.

**P: Como integro com meu projeto Blazor?**
A: A API está pronta para receber requisições HTTP de qualquer cliente.

---

## 📞 Suporte

Veja documentação completa em:
- `README.md` - Documentação detalhada
- `QUICKSTART.md` - Guia rápido (5 min)
- `ARCHITECTURE.md` - Diagramas e fluxos
- `examples.py` - 6 exemplos práticos

---

## ✅ Checklist de Setup

- [ ] `pip install -r requirements.txt`
- [ ] `python pretrained_model.py`
- [ ] `python app.py`
- [ ] `curl http://localhost:5000/health` (testar)
- [ ] Pronto! 🎉

---

**Criado em:** 3 de Dezembro de 2025
**Status:** ✅ Pronto para Produção
**Versão:** 1.0.0

🚀 **Divirta-se testando!**
