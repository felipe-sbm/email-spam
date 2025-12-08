# Detector de Spam - IA

Criei uma API Flask para usar uma IA criada com TensorFlow para detectar spam em mensagens usando Machine Learning (SVM com TF-IDF).

Ela está usando um dataset de mensagens de spam e ham (não spam) para treinar o modelo. Porém está em inglês, portanto precisa ser testado com mensagens em inglês também.

## Estrutura

- `spam_detector.py` - Classe principal com lógica de detecção
- `app.py` - API Flask
- `train.py` - Script para treinar o modelo offline
- `requirements.txt` - Dependências do projeto

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### ⚡ Opção 1: Usar Modelo Pré-Treinado (Recomendado)

Para usar a API sem precisar treinar o modelo toda vez:

```bash
# 1. Gerar modelo pré-treinado (execute UMA VEZ)
python pretrained_model.py

# 2. Iniciar a API
python app.py
```

Isso criará os arquivos:
- `spam_model.pkl` - Modelo SVM pré-treinado
- `vectorizer.pkl` - Vetorizador TF-IDF

**Vantagem:** Rápido, sem necessidade de treinar, pronto para uso imediato!

### 📚 Opção 2: Treinar com Seus Dados

Se você quer treinar com seus próprios dados:

```bash
# 1. Treinar com um CSV customizado
python train.py

# 2. Iniciar a API
python app.py
```

## Uso pessoalizado

## Endpoints

### GET `/health`
Verificar saúde da API

```bash
curl http://localhost:5000/health
```

### GET `/info`
Obter informações sobre a API

```bash
curl http://localhost:5000/info
```

### POST `/predict`
Classificar uma mensagem

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Click here to win $1000!"}'
```

**Resposta:**
```json
{
  "text": "Click here to win $1000!",
  "label": "spam",
  "confidence": 2.34
}
```

### POST `/send` ⭐ **NOVO**
**Enviar mensagem com verificação automática de spam**

Se a mensagem for spam, é **bloqueada**. Se for legítima, é **enviada**.

```bash
# Mensagem bloqueada (spam)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Click here to win $1000!",
    "recipient": "user@example.com"
  }'
```

**Resposta (bloqueada):**
```json
{
  "status": "blocked",
  "reason": "Mensagem identificada como spam",
  "confidence": 2.34,
  "message": "Click here to win $1000!"
}
```

```bash
# Mensagem permitida (ham)
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, como você está?",
    "recipient": "user@example.com"
  }'
```

**Resposta (enviada):**
```json
{
  "status": "sent",
  "message_id": "msg_a1b2c3d4e5f6g7h8",
  "recipient": "user@example.com",
  "message": "Olá, como você está?",
  "timestamp": "2025-12-03T10:30:45.123456"
}
```

### GET `/metrics`
Obter métricas do modelo treinado

```bash
curl http://localhost:5000/metrics
```

**Resposta:**
```json
{
  "accuracy": 0.9543,
  "precision": 0.9234,
  "recall": 0.9876,
  "f1_score": 0.9552,
  "confusion_matrix": [[...], [...]],
  "classification_report": "..."
}
```

### POST `/train`
Treinar o modelo com um novo CSV

```bash
curl -X POST http://localhost:5000/train \
  -H "Content-Type: application/json" \
  -d '{"csv_path": "caminho/para/spam_messages_train.csv"}'
```

## Formato do CSV

O CSV deve ter as colunas:
- `text` - Mensagem de texto
- `label` - Classificação ("spam" ou "ham")

Exemplo:
```
text,label
"Click here to win $1000!",spam
"Meeting tomorrow at 3pm",ham
```

## Exemplo com Python

```python
import requests

# Exemplo 1: Apenas classificar
response = requests.post(
    'http://localhost:5000/predict',
    json={'text': 'Click here to win $1000!'}
)
print(response.json())
# Output: {'text': '...', 'label': 'spam', 'confidence': 2.34}

# Exemplo 2: Enviar mensagem (bloqueado se spam)
response = requests.post(
    'http://localhost:5000/send',
    json={
        'message': 'Olá, como você está?',
        'recipient': 'user@example.com'
    }
)

if response.status_code == 403:
    print("❌ Bloqueado:", response.json()['reason'])
elif response.status_code == 200:
    print("✓ Enviado:", response.json()['message_id'])
```

## Desenvolvimento

Para debug e desenvolvimento:

```bash
export FLASK_ENV=development
python app.py
```

## Notas

- O modelo é persistido em `spam_model.pkl` e `vectorizer.pkl`
- Use TF-IDF para vetorização (padrão em ml.py)
- O modelo SVM usa kernel linear para melhor desempenho
- Confidence é o score da distância do ponto ao hiperplano no SVM
- O modelo é bastante pequeno, ele depende bastante do dataset que vai ser usado.