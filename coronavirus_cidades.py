#!/usr/bin/env python
# coding: utf-8

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


# 1. Grab content from URL (Pegar conteúdo HTML a partir da URL)
url = "https://especiais.g1.globo.com/bemestar/coronavirus/mapa-coronavirus/"

option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(url)
time.sleep(2)

element = driver.find_element_by_xpath("//div[@class='places__body']")
html_content = element.get_attribute('outerHTML')
#print(html_content)


# 2. Parsear o conteúdo HTML - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
#tab = soup.find_all("div", {"class":"places__cell"})
tagCidadeList = soup.find_all("div", {"class":"places__cell"})[0::2]
tagCasosList = soup.find_all("div", {"class":"places__cell"})[1::2]

# Pegando apenas os texto de toda a lista
#dadosCovid = []
#for data in tab:
#    dadosCovid.append(data.get_text())

# Pegando apenas os texto referente as cidades
covidCidades = []
for data in tagCidadeList:
    covidCidades.append(data.get_text())
    
# Pegando apenas os textos referente as quantidades de casos confirmados
covidQtda = []
for data in tagCasosList:
    dataText = data.get_text()
    dataInt = int(dataText)
    covidQtda.append(dataInt)

    
print("Lista das cidades com casos Confirmados: {} \n".format(covidCidades))
print("Lista com as quantidade de casos Confirmados: {} \n".format(covidQtda))

covid = {}
covid['CIDADES'] = covidCidades
covid['CASOS_CONF'] = covidQtda


'''
# Transforma a lista de string para dicionário
alf = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
prfx = alf.split(' ')
covid19={}
key = ''

for city in dadosCovid:
    for p in prfx:
        if p in city:
            key = city
            covid19[key] = []
            break
    if city != key:
        city = int(city)
        covid19[key].append(city)
covid19.items()
print(covid19)
'''


# Criando dataframe no pandas
df = pd.DataFrame(data=covid)
df.columns.values.tolist()
print(df.head())

print("Arquivo exportado para CVC: {}".format(
            df.to_csv("C:\\Users\\BFLH\\Desktop\\COVID.csv")))


driver.quit()

