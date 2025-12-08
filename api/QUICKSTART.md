# 🚀 Guia Rápido - Spam Detector API

## Resumo

Você tem uma **API Flask com IA** que:
- ✅ Detecta spam em mensagens
- ✅ **Bloqueia automaticamente** mensagens spam
- ✅ **Envia apenas** mensagens legítimas
- ✅ Usa um **modelo pré-treinado** (sem necessidade de treinar)

## Setup Inicial (5 minutos)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Gerar modelo pré-treinado (executar UMA VEZ)
python pretrained_model.py

# 3. Iniciar a API
python app.py
```

Pronto! A API está em `http://localhost:5000` ✨

## Testando

### Em outro terminal:

```bash
# Testar todos os endpoints automaticamente
python test_api.py
```

Ou manualmente com curl:

```bash
# ✓ Mensagem legítima (será ENVIADA)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, como vai?", "recipient": "user@example.com"}'

# ❌ Mensagem suspeita (será BLOQUEADA)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Click here to win $1000!", "recipient": "user@example.com"}'
```

## Endpoints Principais

| Endpoint | Método | O que faz |
|----------|--------|----------|
| `/send` | POST | ✅ Envia se legítima, ❌ bloqueia se spam |
| `/predict` | POST | Apenas classifica (sem enviar) |
| `/metrics` | GET | Mostra acurácia do modelo |
| `/health` | GET | Verifica se API está ok |

## Exemplo Python

```python
import requests

# Enviar mensagem (bloqueada se spam)
response = requests.post(
    'http://localhost:5000/send',
    json={
        'message': 'Oi, tudo bem?',
        'recipient': 'amigo@example.com'
    }
)

# Status: 200 (enviada) ou 403 (bloqueada)
if response.status_code == 200:
    print("✓ Mensagem enviada!")
else:
    print("❌ Spam detectado:", response.json()['reason'])
```

## Treinar com Seus Dados

Se quiser usar seus próprios dados de spam/ham:

```bash
python train.py
# Depois reinicie a API
python app.py
```

## Arquivos Importantes

- `app.py` - A API Flask
- `spam_detector.py` - Lógica de detecção
- `pretrained_model.py` - Gera modelo pré-treinado
- `spam_model.pkl` - Modelo IA (criado automaticamente)
- `vectorizer.pkl` - Vetorizador (criado automaticamente)

## Dúvidas Frequentes

**P: Preciso treinar o modelo toda vez?**
R: Não! Execute `python pretrained_model.py` uma vez e pronto. Os arquivos `.pkl` são salvos.

**P: Como funciona a detecção?**
R: Usa SVM com TF-IDF. O modelo aprende padrões de spam (ofertas, links suspeitos, etc).

**P: Posso usar em produção?**
R: Sim! Mude `debug=False` em `app.py` e use um servidor como Gunicorn.

---

**Dúvida?** Veja o README.md completo!
