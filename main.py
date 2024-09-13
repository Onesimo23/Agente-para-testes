from tests.executar_testes import executar_testes

def main():
    print("Executando testes de segurança...")
    
    try:
        # Verificação se a função executar_testes está definida e disponível
        if not callable(executar_testes):
            raise RuntimeError("A função 'executar_testes' não está definida corretamente.")

        # Executar a função de testes
        executar_testes()
    
    except RuntimeError as e:
        print(f"Erro de execução: {e}")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
