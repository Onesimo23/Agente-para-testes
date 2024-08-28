from models.treinamento_modelo import treinar_modelo
from models.geracao_dados import gerar_dados
from tests.executar_testes import executar_testes

def main():
    print("Treinando o modelo...")
    treinar_modelo()
    
    print("Gerando dados...")
    gerar_dados()
    
    print("Executando testes de segurança...")
    executar_testes()

if __name__ == "__main__":
    main()
