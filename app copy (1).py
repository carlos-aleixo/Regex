import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurar o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())

# Criar uma instância do navegador Chrome
driver = webdriver.Chrome(service=service)

# URL do site que você quer acessar
url = 'https://store.steampowered.com/specials/?l=portuguese'

# Carregar a página
driver.get(url)

# Função para rolar até o final da página
def scroll_to_bottom():
    old_position = driver.execute_script("return window.scrollY")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Ajuste conforme a necessidade para esperar o carregamento
        new_position = driver.execute_script("return window.scrollY")
        if new_position == old_position:
            break
        old_position = new_position

# Realizar o scroll
scroll_to_bottom()

# Agora todos os elementos devem estar visíveis
elementos = driver.find_elements(By.CSS_SELECTOR, ".y9MSdld4zZCuoQpRVDgMm")
print(f"Total de elementos carregados: {len(elementos)}")

# Definir a expressão regular para extrair informações
pattern1 = re.compile(r'<div class="Wh0L8EnwsPV_8VAu8TOYr">(.*?)<\/div>')
pattern2 = re.compile(r'<div class="\S* ?StoreSaleWidgetTitle ?\S*">(.*?)<\/div>')
dic = {}

# Iterar sobre cada elemento e aplicar a expressão regular no texto de cada um
for elemento in elementos:
    html_content = elemento.get_attribute('innerHTML')
    matches1 = pattern1.findall(html_content)
    matches2 = pattern2.findall(html_content)
    print(f"Matches found in element: {matches1}")
    print(f"Matches found in element: {matches2}")
    dic[matches2[0]] = matches1[0]

# Fechar o navegador
driver.quit()
print(dic)

# Escrever os dados em um arquivo CSV
csv_filename = "jogos_steam.csv"

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Nome', 'Preço']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for nome, preco in dic.items():
        writer.writerow({'Nome': nome, 'Preço': preco})

print(f"Arquivo CSV '{csv_filename}' criado com sucesso!")