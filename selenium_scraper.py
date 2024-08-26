from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configura o Chrome para rodar em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inicializa o WebDriver com opções headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def abrir_pagina(url):
    driver.get(url)
    time.sleep(2)
    
    # Rolagem para baixo para carregar mais conteúdo, se necessário
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)
    time.sleep(2)

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
    url = f"{base_url}&page={pagina}"
    print(f"Abrindo página {pagina}...")
    
    try:
        questoes = abrir_pagina(url)
        if not questoes:
            print(f"Nenhuma questão encontrada na página {pagina}. Interrompendo.")
            break
        
        todas_questoes.extend(questoes)
        
        if len(todas_questoes) >= 145:
            break
        
        pagina += 1
    
    except Exception as e:
        print(f"Erro ao processar a página {pagina}: {e}")
        break

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
