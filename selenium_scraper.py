from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Caminho para o Tor Browser
tor_browser_path = "/home/jf/Downloads/tor-browser/Browser/firefox-bin"

# Configura o Firefox para usar o Tor
firefox_options = Options()
firefox_options.binary_location = tor_browser_path
firefox_options.add_argument("--headless")  # Descomente se não quiser que o navegador seja visível

# Inicializa o WebDriver com o Tor Browser
driver = webdriver.Firefox(service=Service(), options=firefox_options)

def abrir_pagina(url):
    driver.get(url)
    time.sleep(5)  # Espera a página carregar completamente
    
    # Simula a rolagem para garantir que todos os elementos sejam carregados
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)
    time.sleep(2)  # Espera mais um pouco após rolar

    # Extrai todas as questões com a classe 'q-question-enunciation'
    questoes = driver.find_elements(By.CLASS_NAME, "q-question-enunciation")
    return [questao.text.strip() for questao in questoes if questao.text.strip()]

# URL base da página de questões
base_url = "https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=93&discipline_ids%5B%5D=96&discipline_ids%5B%5D=98&discipline_ids%5B%5D=100&discipline_ids%5B%5D=160&discipline_ids%5B%5D=503&exclude_outdated=true&institute_ids%5B%5D=14&my_questions=all"
pagina = 1

# Lista para armazenar todas as questões
todas_questoes = []

# Loop para iterar pelas páginas até coletar 145 questões
while len(todas_questoes) < 145:
    # Cria a URL para a página atual
    url = f"{base_url}&page={pagina}"
    print(f"Abrindo página {pagina}...")
    
    questoes = abrir_pagina(url)
    if not questoes:
        print(f"Nenhuma questão encontrada na página {pagina}. Interrompendo.")
        break

    todas_questoes.extend(questoes)

    # Incrementa o número da página
    pagina += 1

# Fecha o navegador
driver.quit()

# Exibe o total de questões coletadas e salva em um arquivo
total_questoes = len(todas_questoes)
print(f"Total de questões coletadas: {total_questoes}")

# Salva as questões em um arquivo de texto
with open('questoes.txt', 'w', encoding='utf-8') as file:
    for questao in todas_questoes:
        file.write(questao + '\n')

print("Questões foram salvas em 'questoes.txt'")
