from zapv2 import ZAPv2 # type: ignore
import requests
from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin
from models.geracao_dados import gerar_dados
from models.treinamento_modelo import treinar_modelo

# Configuração do ZAP
apiKey = input('\n\tInsira a API da ZAP:')
zap = ZAPv2(apikey= apiKey, proxies={'http': 'http://127.0.0.1:8080'})

# Função para pegar formulários do site
def get_forms(url):
    # Adicionar esquema se estiver faltando
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção para erros HTTP
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o URL: {e}")
        return []

def form_details(form):
    details_of_form = {}
    action = form.attrs.get("action", "")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })
    
    details_of_form['action'] = action
    details_of_form['method'] = method
    details_of_form['inputs'] = inputs

    return details_of_form

# Função para executar testes de SQL Injection
def sql_injection_scan(url):
    forms = get_forms(url)
    print(f"[+] Detectado {len(forms)} formulários em {url}.")
    if not forms:
        return

    for form in forms:
        details = form_details(form)
        inputs = details["inputs"]
        action = form.attrs.get("action", "")
        method = form.attrs.get("method", "get").lower()
        form_url = urljoin(url, action) if action else url

        # Teste de SQL Injection
        data = {input_tag.get("name"): "Test'" for input_tag in form.find_all("input") if input_tag.get("name")}
        try:
            res = requests.post(form_url, data=data) if method == "post" else requests.get(form_url, params=data)
            if "syntax" in res.text.lower():
                print(f"[!] Vulnerabilidade de SQL Injection detectada em {form_url}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao testar SQL Injection: {e}")

# Função para executar testes de XSS
def xss_scan(url):
    print(f"Executando teste de XSS em {url}...")
    # Aqui podes adicionar lógica de teste de XSS
    print("Nenhuma vulnerabilidade XSS detectada.")

# Função principal de execução de testes
def executar_testes():

    print("\n\t\t============== Agente de Teste de Vulnerabilidades ==============")
    print("\n\n\t\t=================== Seja Bem Vindo ==================")
    print("\nO presente programa visa auxiliar os seus usuários a realizarem testes de vulnerabilidades nos seus sites ou sistemas")
    
    zap = ZAPv2(apikey='ma9kcjhk4a1ihk1qssmjlrq2ps', proxies={'http': 'http://127.0.0.1:8080'})

    print("\nEscolha o tipo de teste a ser realizado:")
    print("\n\n\n\t\t\t1 - SQL Injection\n\t\t\t2 - XSS\n\t\t\t3 - DDoS")
    choice = input("Escolha a opção: ").strip()

    if choice == "1":
        url = input("Insira o URL para teste de vulnerabilidades: ").strip()
        print("Treinando o modelo...")
        treinar_modelo()
        print("Gerando dados...")
        gerar_dados()
        print('Iniciando varredura ativa...')
        zap.ascan.scan(url)
        print('Varredura ativa iniciada.')
        sql_injection_scan(url)
    elif choice == "2":
        url = input("Insira o URL para teste de vulnerabilidades: ").strip()
        xss_scan(url)
    elif choice == "3":
         print("\n\tAguarde o dev...")
    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")
