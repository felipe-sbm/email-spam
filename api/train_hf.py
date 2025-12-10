import os
import pandas as pd
from datasets import load_dataset
from app.utils.spam_detector import SpamDetector

def main():
    print("Carregando dataset 'ucirvine/sms_spam' do Hugging Face...")
    try:
        dataset = load_dataset("ucirvine/sms_spam", split="train")
    except Exception as e:
        print(f"Erro ao carregar dataset: {e}")
        return

    print("Convertendo para DataFrame...")
    df = pd.DataFrame(dataset)
    
    # O dataset tem colunas 'sms' e 'label' (0=ham, 1=spam)
    # Vamos renomear 'sms' para 'text' e mapear 'label' para 'ham'/'spam'
    
    if 'sms' in df.columns:
        df = df.rename(columns={'sms': 'text'})
    
    if 'label' in df.columns:
        # Verificar se é numérico
        if pd.api.types.is_numeric_dtype(df['label']):
            df['label'] = df['label'].map({0: 'ham', 1: 'spam'})
    
    # Salvar em CSV temporário para usar com SpamDetector.load_data
    csv_path = 'data/sms_spam_hf.csv'
    os.makedirs('data', exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Dataset salvo em {csv_path}")
    
    # Inicializar detector
    detector = SpamDetector()
    
    print(f"\nCarregando dados de {csv_path}...")
    X, y = detector.load_data(csv_path)
    
    print(f"Total de mensagens carregadas: {len(X)}")
    print(f"Distribuição de classes:\n{y.value_counts()}\n")
    
    print("Treinando modelo... (isso pode levar alguns minutos)")
    X_test, y_test, y_pred = detector.train(X, y)
    
    print("\n=== Métricas do Modelo ===")
    metrics = detector.get_metrics()
    print(f"Acurácia: {metrics['accuracy']:.4f}")
    print(f"Precisão: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")
    
    # Salvar modelo
    print("\nSalvando modelo...")
    detector.save_model()
    
    print("\n✓ Modelo treinado e salvo com sucesso!")

if __name__ == '__main__':
    main()
