import requests

def monitorar_respostas(url):
    """
    Monitora e analisa as respostas da aplicação para identificar falhas.
    """
    try:
        response = requests.get(url)
        status_code = response.status_code
        content = response.text
        
        print(f"Status Code: {status_code}")
        print("Primeiros 500 caracteres da resposta:")
        print(content[:500])  # Mostrar apenas os primeiros 500 caracteres para análise
        
        # Simples verificação para demonstrar
        if status_code != 200:
            print("Atenção: A aplicação retornou um status code diferente de 200.")
        
        if "vulnerabilidade" in content.lower():
            print("Atenção: A resposta contém possíveis indicadores de vulnerabilidade.")
    
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")

if __name__ == "__main__":
    url = 'https://unisave.ac.mz/'  
    monitorar_respostas(url)
