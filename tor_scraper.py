from bs4 import BeautifulSoup
import requests
from collections import Counter
from requests.exceptions import RequestException
from stem import Signal
from stem.control import Controller

# Configuração do proxy para Tor
PROXY = 'socks5h://127.0.0.1:9050'

# Função para obter uma nova identidade do Tor
def renew_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_control_password')
        controller.signal(Signal.NEWNYM)

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
