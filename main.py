import time 
from pandas import DataFrame
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

db = open("file.txt", 'r')
tdata = db.read()
data = tdata.splitlines()
urls = []

servico = Service(GeckoDriverManager().install())

navegador = webdriver.Firefox(service=servico)

for name in data:
    navegador.get("http://buscatextual.cnpq.br/buscatextual/busca.do")

    navegador.find_element('xpath', '//*[@id="textoBusca"]').send_keys(name)
    navegador.find_element('xpath', '//*[@id="buscarDemais"]').click()
    navegador.find_element('xpath', '//*[@id="botaoBuscaFiltros"]').click()

    time.sleep(2)
    
    try:
        navegador.find_element('xpath', '/html/body/form/div/div[4]/div/div/div/div[3]/div/div[3]/ol/li/b/a').click()

        time.sleep(2)

        navegador.find_element('xpath', '//*[@id="idbtnabrircurriculo"]').click()

        time.sleep(1)

        handles = navegador.window_handles
        navegador.switch_to.window(handles[1])

        time.sleep(2)
        print(navegador.current_url)
        urls.append(navegador.current_url)

        navegador.close()
        time.sleep(1)
        navegador.switch_to.window(handles[0])
        time.sleep(2)
        
    except:
        print('none')
        urls.append('none')
    
df = DataFrame({"Nomes": data, "Currículo Lattes" : urls})
df.to_excel('lattes.xlsx', sheet_name = 'sheet1', index=False)
