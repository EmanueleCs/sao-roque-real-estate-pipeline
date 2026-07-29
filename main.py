from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import openpyxl
import os

driver = webdriver.Chrome()
conteudo = driver.get("https://www.guiasaoroque.com.br/imoveis/")

driver.implicitly_wait(10)

# Seleciona 'Aluguel'
botao = driver.find_element(By.XPATH, "//*[@id='searchFormIndex2']/div[1]/div/button[2]")
botao.click()

# Seleciona 'Apartamentos'
botao = driver.find_element(By.XPATH, "//*[@id='containerTipoIndex2']/div[1]")
botao.click()
botao = driver.find_element(By.XPATH, "//*[@id='optionsTipoIndex2']/label[2]")
botao.click()

# Clica em 'Busca'

botao = driver.find_element(By.XPATH, "//*[@id='submitBtnIndex2']")
botao.click()

qtde_paginas = driver.find_element(By.XPATH, "//*[@id='formPaginaListagem']/span")
qtde_paginas = qtde_paginas.text
qtde_paginas = int(qtde_paginas.replace('de ', '')) + 1

lista = []
links = []
for pagina in range(1, qtde_paginas):
    driver.get(f"https://www.guiasaoroque.com.br/imoveis/alugar/sao-roque/apartamentos?transacao=aluguel&categoria%5B0%5D=apartamento&page={pagina}")
    # Seleciona preço
    conjunto_cards = driver.find_element(By.XPATH, "//*[@id='propertiesGrid']")
    cards = conjunto_cards.find_elements(By.TAG_NAME, "article")

    for card in cards:
            link_imovel = card.find_element(By.XPATH, "./div[2]/div[5]/a")
            href = link_imovel.get_attribute('href')

            links.append(href)

def texto_seguro(by, valor):
    try:
        elemento = driver.find_element(by, valor)
        return elemento.text
    except NoSuchElementException:
        return ''

resultado = []

for link in links:
    driver.get(link)

    dados_imovel = {
        "titulo": texto_seguro(By.TAG_NAME, "h1"),
        "preco": texto_seguro(By.XPATH, "/html/body/main/div/div[1]/div[2]/div[1]/div"),
        "descricao": texto_seguro(By.XPATH, "/html/body/main/div/div[2]/div[1]/div[3]/div/p"),
        "codigo_imovel": texto_seguro(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div/div[1]/span[2]"),
        "codigo_interno": texto_seguro(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div/div[2]/span[2]"),
        "imobiliaria": texto_seguro(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[1]/div[1]/a[2]"
    ),
}

    print(dados_imovel)
    resultado.append(dados_imovel)
print(resultado)

# df = pd.DataFrame(resultado)
# df.to_excel('resultado.xlsx', index=False)

driver.implicitly_wait(5)

driver.close()