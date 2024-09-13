import requests
from datetime import datetime
from fpdf import FPDF # type: ignore

# Função para gerar relatório em PDF
def gerar_relatorio_pdf(resultados, url):
    data_monitoramento = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    pdf = FPDF()
    pdf.add_page()

    # Título do Relatório
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Relatório de Testes de Vulnerabilidade", ln=True, align='C')
    
    # Informações gerais
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"URL monitorada: {url}", ln=True)
    pdf.cell(200, 10, f"Data e Hora do Monitoramento: {data_monitoramento}", ln=True)
    pdf.cell(200, 10, f"Total de testes realizados: {len(resultados)}", ln=True)

    # Resultados dos testes
    pdf.ln(10)
    for result in resultados:
        pdf.cell(200, 10, f"Data e Hora: {result['data_hora']}", ln=True)
        pdf.cell(200, 10, f"Status Code: {result['status_code']}", ln=True)
        pdf.cell(200, 10, f"Vulnerabilidade: {result['vulnerabilidade']}", ln=True)
        pdf.cell(200, 10, f"Primeiros 500 caracteres da resposta: {result['conteudo']}", ln=True)
        pdf.ln(10)

    # Salvar o PDF
    pdf.output(f"reports/report_monitoramento_{data_monitoramento}.pdf")
    print("Relatório em PDF gerado com sucesso.")

# Função para monitorar e analisar as respostas da aplicação
def monitorar_respostas(url):
    """
    Monitora e analisa a resposta da aplicação para identificar falhas.
    """
    resultados = []
    try:
        response = requests.get(url)
        status_code = response.status_code
        content = response.text
        
        print(f"Status Code: {status_code}")
        print("Primeiros 500 caracteres da resposta:")
        print(content[:500])  # Mostrar apenas os primeiros 500 caracteres para análise
        
        # Simples verificação para demonstrar
        if status_code != 200:
            resultados.append({
                'data_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status_code': status_code,
                'vulnerabilidade': 'Status Code diferente de 200',
                'conteudo': content[:500]
            })
        
        if "vulnerabilidade" in content.lower():
            resultados.append({
                'data_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status_code': status_code,
                'vulnerabilidade': 'Conteúdo contém indicadores de vulnerabilidade',
                'conteudo': content[:500]
            })

    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")

    return resultados

if __name__ == "__main__":
    url = input("Insira o URL para monitoramento: ").strip()
    resultados = monitorar_respostas(url)
    gerar_relatorio_pdf(resultados, url)
