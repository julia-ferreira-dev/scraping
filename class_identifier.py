from bs4 import BeautifulSoup
import requests
from collections import Counter

# URL da página a ser analisada
url = "https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=93&discipline_ids%5B%5D=96&discipline_ids%5B%5D=98&discipline_ids%5B%5D=100&discipline_ids%5B%5D=160&discipline_ids%5B%5D=503&exclude_outdated=true&institute_ids%5B%5D=14&my_questions=all"

# Define os headers para simular uma requisição de navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.84 Safari/537.36'
}

# Faz a requisição para a URL com os headers
response = requests.get(url, headers=headers)
response.raise_for_status()

# Cria o BeautifulSoup para analisar o HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Encontra todos os elementos com classes
classes = [cls for elem in soup.find_all(class_=True) for cls in elem.get('class')]

# Conta a frequência das classes
contagem_classes = Counter(classes)

# Exibe as classes mais comuns
print("Classes mais comuns:")
for classe, contagem in contagem_classes.most_common():
    print(f"{classe}: {contagem}")
