# Correio Eletrônico - IA

Neste projeto desenvolvi um sistema de Inteligência Artificial que detecta e-mails que possam ser possíveis fraudes, golpes e até mesmo mensagens desnecessárias.

Este sistema foi feito com `Flask`, `TensorFlow` e `Blazor (C#)` com`Wasm (Web Assembly 💀)`. A IA pensa, retorna ao usuário através da API feita com Flash e tudo é exibido ao usuário através da UI feita com o Framework Blazor.

## Começando
### Requisitos
- Python 3.8+
- .NET 7 SDK
- Navegador moderno (Chrome, Edge, Firefox ou Safari)

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/email-spam.git
cd email-spam
```
2. Configure a API:
```bash
cd api
pip install -r requirements.txt
python pretrained_model.py
python app.py
```
3. Inicie a UI:
```bash
cd ../ui
dotnet run
```

4. Acesse a UI no navegador:
```bash
http://localhost:5110
```

## O Uso
Envie e-mails através da UI e a IA analisará o conteúdo para detectar possíveis spams ou fraudes, bloqueando mensagens suspeitas automaticamente.

## Como Funciona a IA
A IA utiliza um modelo de Aprendizado de Máquina baseado em SVM (Support Vector Machine) com vetorização TF-IDF para classificar as mensagens como legítimas ou spam. Ela foi treinada com um conjunto de dados de mensagens de spam e ham (não spam) para aprender a identificar padrões comuns em mensagens fraudulentas.
- Use TF-IDF para vetorização (padrão em ml.py)
- O modelo SVM usa kernel linear para melhor desempenho
- Confidence é o score da distância do ponto ao hiperplano no SVM
- O modelo é bastante pequeno, ele depende bastante do dataset que vai ser usado.

## Contribuição
Como isso foi um projeto para o trabalho da terceira unidade de Aprendizado de Maquina, e não será publicado nem atualizado, sinta-se à vontade para explorar o código, aprender e adaptar para seus próprios projetos dando um fork. Para me ajudar, de uma estrela no repositório! ⭐ Ficarei muito feliz!

## Com Licença, senhor... (piadas ruins)
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE). Coloquei somente para não ter problemas futuros (independentemente do que seja 😳), mas como é um projeto acadêmico, sinta-se livre para usar como quiser.