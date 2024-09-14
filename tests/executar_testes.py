from zapv2 import ZAPv2  # type: ignore
import requests
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin
from models.geracao_dados import gerar_dados
from models.treinamento_modelo import treinar_modelo
import os
from fpdf import FPDF  # type: ignore
import threading
import time
import re


def sanitize_filename(filename):
    # Substitui todos os caracteres inválidos por "_"
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

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
    
    nome_site_sanitized = sanitize_filename(nome_site)
    relatorio_path = os.path.join('reports', f'relatorio_de_{nome_site_sanitized}.pdf')
    pdf.output(relatorio_path)
    print(f"Relatório salvo como {relatorio_path}")


# Função para pegar formulários do site
def get_forms(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

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
            else:
                resultados.append(f"SQL Injection não detectado no formulário {form_url}")
        except requests.exceptions.RequestException as e:
            resultados.append(f"Erro ao testar SQL Injection: {e}")
    
    return resultados


# Função para executar testes de XSS
def xss_scan(url):
    resultados = []
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
def ddos_attack_simulation(url, num_requests, delay=0):
    print(f"Simulando ataque DDoS em {url} com {num_requests} requisições...")
    resultados = []

    def send_request():
        try:
            response = requests.get(url)
            resultados.append(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            resultados.append(f"Erro ao realizar requisição DDoS: {e}")
    
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()
        time.sleep(delay)  # Controlar o tempo entre as requisições

    for thread in threads:
        thread.join()

    print("Simulação de ataque DDoS concluída.")
    return resultados


# Função principal de execução de testes
def executar_testes():
    print("\n\t\t============== Agente de Teste de Vulnerabilidades ==============")
    print("\n\n\t\t=================== Seja Bem Vindo ==================")
    print("\nO presente programa visa auxiliar os seus usuários a realizarem testes de vulnerabilidades nos seus sites ou sistemas")
    
    zap_ip = input("Insira o IP da ZAP: ").strip()
    zap_api_key = input("Insira a API da ZAP: ").strip()
    zap = ZAPv2(apikey=zap_api_key, proxies={'http': f'http://{zap_ip}:8080'})

    resultados = []  # Lista para armazenar todos os resultados
    
    print("\nEscolha o tipo de teste a ser realizado:")
    print("\n\t1 - SQL Injection\n\t2 - XSS\n\t3 - DDoS\n\t4 - Todos os ataques")
    choice = input("Escolha a opção: ").strip()

    url = input("Insira o URL para teste de vulnerabilidades (ex: http://localhost/dvwa): ").strip()
# url para testes sql: http://testphp.vulnweb.com/
    if choice == "3" or choice == "4":
        num_requests = int(input("Digite o número de requisições para o ataque DDoS: ").strip())
        delay = float(input("Digite o intervalo entre as requisições (em segundos): ").strip())
    else:
        num_requests = 0
        delay = 0

    if choice == "1" or choice == "4":
        print("Iniciando varredura SQL Injection...")
        resultados_sql_injection = sql_injection_scan(url)  # Chama o teste de SQL Injection
        resultados.extend(resultados_sql_injection)  # Adiciona os resultados à lista

    if choice == "2" or choice == "4":
        print("Iniciando varredura XSS...")
        resultados_xss = xss_scan(url)  # Chama o teste de XSS
        resultados.extend(resultados_xss)  # Adiciona os resultados à lista

    if choice == "3" or choice == "4":
        print("Iniciando simulação de ataque DDoS...")
        ddos_results = ddos_attack_simulation(url, num_requests, delay)  # Chama o teste de DDoS
        resultados.extend(ddos_results)  # Adiciona os resultados à lista

    if not resultados:
        resultados.append("Nenhuma vulnerabilidade foi encontrada nos testes executados.")

    criar_relatorio_pdf(url, resultados)  # Gera o relatório com os resultados finais
