from spam_detector import SpamDetector
import sys


def main():
    # Caminho para o arquivo CSV de treinamento
    # Você pode ajustar este caminho conforme necessário
    csv_path = input("Digite o caminho do arquivo CSV para treinar (ex: spam_messages_train.csv): ").strip()
    
    if not csv_path:
        print("Caminho inválido!")
        sys.exit(1)
    
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
    
    print("\nMatriz de Confusão:")
    print(metrics['confusion_matrix'])
    
    print("\n=== Relatório de Classificação ===")
    print(metrics['classification_report'])
    
    # Salvar modelo
    print("\nSalvando modelo...")
    detector.save_model()
    
    print("\n✓ Modelo treinado e salvo com sucesso!")
    print("Agora você pode iniciar a API com: python app.py")


if __name__ == '__main__':
    main()
