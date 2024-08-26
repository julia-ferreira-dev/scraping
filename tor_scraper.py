from bs4 import BeautifulSoup
import requests
from collections import Counter
from requests.exceptions import RequestException
from stem import Signal
from stem.control import Controller
import time

# Configuração do proxy para Tor
PROXY = 'socks5h://127.0.0.1:9050'
TOR_CONTROL_PORT = 9051

# Função para obter uma nova identidade do Tor
def renew_tor_identity():
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.signal(Signal.NEWNYM)
            time.sleep(10)  # Aguarda o Tor criar um novo circuito
            print("Identidade do Tor renovada.")
    except Exception as e:
        print(f"Erro ao renovar a identidade do Tor: {e}")

# Função para fazer a requisição usando Tor
def tor_get(url):
    try:
        response = requests.get(url, proxies={'http': PROXY, 'https': PROXY})
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None

# URL da página a ser analisada
url = "https://www.qconcursos.com/"

# Obtém uma nova identidade do Tor para evitar bloqueios
renew_tor_identity()

# Faz a requisição para a URL usando Tor
html = tor_get(url)
if html:
    # Cria o BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Encontra todos os elementos com classes
    classes = [cls for elem in soup.find_all(class_=True) for cls in elem.get('class')]

    # Conta a frequência das classes
    contagem_classes = Counter(classes)

    # Exibe as classes mais comuns
    print("Classes mais comuns:")
    for classe, contagem in contagem_classes.most_common():
        print(f"{classe}: {contagem}")
else:
    print("Não foi possível obter o conteúdo da página.")
