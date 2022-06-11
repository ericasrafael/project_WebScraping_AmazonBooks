# %%

# -------------------------------------------------------Importando Bibliotecas
from selenium import webdriver  # abrir navegador
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  # extrair de código html
import pandas as pd
import time

# %%

# ---------------------------------------------------Navegando até site da Amazon
#options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
driver = webdriver.Firefox()
driver.get('https://www.amazon.com.br/')
print(driver.title)
time.sleep(8)

# %%

# ---------------------Selecionando o campo de busca e inserindo o termo de busca
input_busca = driver.find_element(
    By.XPATH, value="//*[@id='twotabsearchtextbox']")
input_busca.send_keys('Livros Business Intelligence')
time.sleep(2)
# ---------------------------------------------------------------Enter para buscar
input_busca.send_keys(Keys.ENTER)
time.sleep(8)

# %%

print(driver.title)

# informação presente sempre na primeira página da pesquisa
page_delimiter = int(driver.find_elements(
    By.CSS_SELECTOR, '.s-pagination-item.s-pagination-disabled')[1].text)

elements_list = []

for page in range(1, page_delimiter+1):

    # extrair de código html a cada mudança de página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    # carregar novos itens-books a cada mudança de página
    books = soup.select(
        "div.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.s-widget-spacing-small.sg-col-4-of-20")

    time.sleep(2)

    for book in books:

        # Título
        t = book.select(
            'span[class="a-size-base-plus a-color-base a-text-normal"]')[0]
        titulo = t.get_text()

        # Autor
        autors = book.select('span[class="a-size-base"]')
        if(len(autors) != 0):
            a = book.select('span[class="a-size-base"]')[1]
            autor = a.get_text()
        else:
            autor = ""

        # Link
        l = book.select(
            'a[class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')[0]
        link = l.get('href')

        # Preço
        prices = book.select('span[class="a-offscreen"]')
        if(len(prices) != 0):
            p = book.select('span[class="a-offscreen"]')[0]
            preco = p.get_text()
        else:
            preco = ""

        elements_list.append([titulo, autor, link, preco])

    try:
        btn_proximo = driver.find_element(
            By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
        btn_proximo.click()
        print(f'\u001b[32m{"Navegando para proxima pagina"}\u001b[0m')
        time.sleep(2)
    except:
        print(f'\u001b[33m{"Não há mais paginas!"}\u001b[0m')
        print(f'\u001b[32m{"Escaneamento Concluido"}\u001b[0m')


pd.DataFrame(elements_list, columns=['Título', 'Autor', 'Link', 'Preço'])

# %%
btn_proximo = driver.find_element(
    By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
btn_proximo.click()
print(f'\u001b[32m{"Navegando para proxima pagina"}\u001b[0m')
time.sleep(2)

# %%


# %%
