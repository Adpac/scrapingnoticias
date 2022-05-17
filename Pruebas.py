import random
from time import sleep
from webbrowser import get
from selenium import webdriver


driver= webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.eldiario.net/portal/')
#todos los anuncios en una lista
noticias=driver.find_elements_by_xpath("//article[@class='jeg_post jeg_pl_sm format-standard']")
for noticia in noticias:
    url=noticia.find_element_by_xpath("//a[@class]")
    print("noticia: ",noticia)
    print(url.get_attribute("href"))

