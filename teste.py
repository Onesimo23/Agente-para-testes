# from zapv2 import ZAPv2

# zap = ZAPv2(apikey='d5slmerpfcvl5au2946cqd8stn', proxies={'http': 'http://127.0.0.1:8080'})

# print('ZAP Version: ' + zap.core.version)
from zapv2 import ZAPv2

def executar_testes():
    zap = ZAPv2(apikey='d5slmerpfcvl5au2946cqd8stn', proxies={'http': 'http://127.0.0.1:8080'})
    url = ''

    print('Iniciando varredura ativa...')
    zap.ascan.scan(url)
    print('Varredura ativa iniciada.')

if __name__ == "__main__":
    executar_testes()
