from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime
from selenium.webdriver.chrome.options import Options
import os

def load_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    content = driver.get("https://www.guiasaoroque.com.br/imoveis/")

    driver.implicitly_wait(10)

    # Select 'Rent'
    button = driver.find_element(By.XPATH, "//*[@id='searchFormIndex2']/div[1]/div/button[2]")
    button.click()

    # Select 'Apartments'
    button = driver.find_element(By.XPATH, "//*[@id='containerTipoIndex2']/div[1]")
    button.click()
    button = driver.find_element(By.XPATH, "//*[@id='optionsTipoIndex2']/label[2]")
    button.click()

    # Write "1600" for the max price
    max_price_input = driver.find_element(By.XPATH, "//*[@id='maxPriceIndex2']")
    max_price_input.send_keys("1600")

    # Click 'Search'
    button = driver.find_element(By.XPATH, "//*[@id='submitBtnIndex2']")
    button.click()

    return driver

def get_page_count(driver):
    try:
        page_count = driver.find_element(By.XPATH, "//*[@id='formPaginaListagem']/span")
        print(page_count)
        page_count = page_count.text
        page_count = int(page_count.replace('de ', '')) + 1
        return driver, page_count
    except NoSuchElementException:
        page_count = 1
        return driver, page_count

def list_cards(driver, page_count):
    card_list = []
    for page in range(0, page_count):
        if page_count > 1:
            driver.get(f"https://www.guiasaoroque.com.br/imoveis/alugar/sao-roque/apartamentos?transacao=aluguel&categoria%5B0%5D=apartamento&page={page}")

        else:
            driver.get(f"https://www.guiasaoroque.com.br/imoveis/alugar/sao-roque/apartamentos?max_preco=1600")

        cards_container = driver.find_element(By.XPATH, "//*[@id='propertiesGrid']")
        cards = cards_container.find_elements(By.TAG_NAME, "article")
        card_list.extend(cards)
    return card_list

def build_links(cards):
    links = []

    for card in cards:
            property_link = card.find_element(By.XPATH, "./div[2]/div[5]/a")
            href = property_link.get_attribute('href')
            links.append(href)
    return links

def safe_text(by, value, driver):
    try:
        element = driver.find_element(by, value)
        return element.text
    except NoSuchElementException:
        return ''

def process_properties(driver, links):
    result = []
    for link in links:
        driver.get(link)

        property_data = {
            "title": safe_text(By.TAG_NAME, "h1", driver),
            "price": safe_text(By.XPATH, "/html/body/main/div/div[1]/div[2]/div[1]/div", driver),
            "description": safe_text(By.XPATH, "/html/body/main/div/div[2]/div[1]/div[3]/div/p", driver),
            "property_code": safe_text(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div/div[1]/span[2]", driver),
            "internal_code": safe_text(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[3]/div/div[2]/span[2]", driver),
            "real_estate_agency": safe_text(By.XPATH, "/html/body/main/div/div[2]/div[2]/div[1]/div[1]/a[2]", driver),
            "link": link
        }

        result.append(property_data)
    return result

def save_csv(result):
    df = pd.DataFrame(result)
    raw_date = datetime.datetime.now()
    formatted_date = raw_date.strftime("%d-%m-%Y-%H-%M")
    path = "results/"
    os.makedirs(path, exist_ok=True)
    df.to_csv(f"results/result-{formatted_date}.csv", index=False)

def orchestrator():
    data = load_data()
    driver, page_count = get_page_count(data)
    data = list_cards(driver, page_count)
    data = build_links(data)
    data = process_properties(driver, data)
    save_csv(data)

    driver.implicitly_wait(5)
    driver.close()

if __name__ == "__main__":
    orchestrator()