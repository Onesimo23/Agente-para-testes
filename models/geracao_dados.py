import random
import string

def gerar_dados():
    """
    Gera dados de teste para simular inputs maliciosos.
    """
    sql_injection_payloads = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' AND 1=2 UNION SELECT NULL, username, password FROM users --",
    "' OR '1'='1' #",
    "' OR '1'='1' /*"
]

    
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<input type=\"text\" value=\"<script>alert(1)</script>\">"
    ]


    
    # Geração de dados aleatórios
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    generated_data = {
        'sql_injection': random.choice(sql_injection_payloads),
        'xss': random.choice(xss_payloads),
        'random_string': random_string()
    }
    
    print("Dados gerados:")
    for key, value in generated_data.items():
        print(f"{key}: {value}")

# if __name__ == "__main__":
#     gerar_dados()
