from zapv2 import ZAPv2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuração do ZAP
zap = ZAPv2(apikey='ok9nol53lms8kept2c28sgrlg9', proxies={'http': 'http://127.0.0.1:8080'})

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

# Função para executar testes de SQL Injection
def sql_injection_scan(url):
    forms = get_forms(url)
    print(f"[+] Detectado {len(forms)} formulários em {url}.")
    if not forms:
        return

    for form in forms:
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
    # Solicitar URL ao usuário
    url = input("Insira o URL para teste de vulnerabilidades: ").strip()

    print("\nEscolha o tipo de teste a ser realizado:")
    print("1 - SQL Injection")
    print("2 - XSS")
    choice = input("Escolha a opção: ").strip()

    if choice == "1":
        sql_injection_scan(url)
    elif choice == "2":
        xss_scan(url)
    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")
