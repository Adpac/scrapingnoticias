from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import lxml.html as html
import re
from selenium import webdriver

#Obtimizar algoritmo, hay cosas innesesarias
def obtenerurlsec(URLPadre):
    if URLPadre[-1]=="/":
        URLPadre=URLPadre[0:-1]
    datos='//ul//a/@href'
    r=requests.get(URLPadre)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    categorias=parser.xpath(datos)
    urls=eliminarrepe(categorias)
    urls=filtrarsolosubdominios(urls,URLPadre)
    urls=eliminarvacios(urls,URLPadre)
    return(urls)
    
def obtenerenlaces(URLPadre, xpath):
    arrayhtml=URLPadre.split("/")
    if URLPadre[-1]=="/":
        URLPadre=URLPadre[0:-1]
    datos=xpath+"//@href"
    print("Xpath datos......: ", datos)
    print("urlpadre: ", URLPadre)
    r=requests.get(URLPadre)
    parser=html.fromstring(r.content)
    categorias=parser.xpath(datos)
    print(categorias)
    urls=eliminarrepe(categorias)
    urls=filtrarsolosubdominios(urls,URLPadre)
    urls=eliminarvacios(urls,URLPadre)
    print("lista urls: ",urls)
    return(urls)

def obtenerurls(URLPadre, esdinamica=True):
    datos='//ul//a/@href'
    r=requests.get(URLPadre)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    categorias=parser.xpath(datos)
    urls=eliminarrepe(categorias)
    urls=filtrarsolosubdominios(urls,URLPadre)
    urls=eliminarvacios(urls,URLPadre)

    if not esdinamica:
        urls=descartarurls(urls)
        urls=filtrarnumeracion(urls)
    return(urls)
def filtrarsolosubdominios(lista,urlP): 
    #Filtramos los dominios que no contengan la url principal
    #Algunos sub dominios empiezan con /url pero pertenecen al subdominio
    arrayurlp=urlP.split("/")
    urlP=arrayurlp[0]+"//"+arrayurlp[2]
    listaaux=[]
    for url in lista:
        if not "http" in url[0:4]:
            if urlP[-1]=="/":
                url=urlP[0:-1]+url
            else:
                url=urlP+url
        
        if urlP in url:

            listaaux.append(url)

    return listaaux

def eliminarrepe(lista):
    resultantList = []

    
    for element in lista:
        if element[-1]=="/":
            element=element[0:-1]
        if element not in resultantList:
            resultantList.append(element)
    return resultantList

def eliminarvacios(lista,urlprincipal):
    aux=[]
    for element in lista:
        if element != "#" and element != urlprincipal and element != urlprincipal+"#" and element !="":
            print("Elemento: ",element)
            #print("Elemento: ",str(element).index(str(urlprincipal)))
            if element.find(urlprincipal)==0:
                aux.append(element)
    return aux

   #Encontramos las sub urls de las paginas web 
def contienesuburl(urlPag):
    #print ("URL: ", urlPag)
    retornar=False
    try:
        r1=requests.get(urlPag)
        decode=r1.content.decode('utf-8')
        parser=html.fromstring(decode)
        urls=parser.xpath("//a/@href")
        urls=filtrarsolosubdominios(urls,urlPag)
        for url in urls:
            if urlPag in url and url != urlPag:
                retornar=True
                break
    except:
        retornar=False         
    return retornar
def encontrarsuburls(urlPag):
    r=requests.get(urlPag)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    urls=parser.xpath("//a/@href")
    suburls=[]
    for url in urls:
        if urlPag in url and url != urlPag:
            suburl=url.replace(urlPag,"")
            suburls.append(suburl)
    return suburls

def descartarurls(listaurls):
    aux=[]  #descartamos aquellas sub urls que no contienen paginacion
    for lista in listaurls:
        if contienesuburl(lista):
            print ("URL: ", lista, "TRUE")
            aux.append(lista)
            
    return aux

#Ahora solo queda descubrir un patron para encontrar el xpath del boton siguiente
#//a[contains(@href,"https://www.eldiario.net/portal/category/deportes/page/2/")]//@*
#//a[contains(@href,"https://www.la-razon.com/nacional/")]//@*

#//a[contains(@href,"https://www.eldiario.net/portal/category/sociales/") and text()>0]//text()
#En lugar de conseguir un xpath podemos descubrir 

def obtenernumeracionpag(urlP):
    xpathnumurl='//a[text()>0]//@href'
    xpathnumtext='//a[text()>0]//text()'
    r=requests.get(urlP)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    
    listaurls=parser.xpath(xpathnumurl)
    listnum=parser.xpath(xpathnumtext)
    listaurls=filtrarsolosubdominios(listaurls,urlP)
    #print(set(listaurls))
    print("--------------------")
    string=""
    numeroinicial=1
    numerofinal=-10

    for i, url in enumerate(listaurls):
        #print("Pagina web: ",url, "Pagina: ", i)
        numero = [int(temp)for temp in re.split(r'[/?=]',url) if temp.isdigit()][0]
        #print(numero)
        #print(xpathnumtext)
        #print("NUMERO TEXT: ",listnum[i])
        if  i==0:
            if numero>int(listnum[i]):
                numeroinicial=0
        if numerofinal<numero:
            numerofinal=numero

        string=url.replace(str(numero),"(n)")
        #print("-------------")
    string=string[len(urlP):]
    return string,numeroinicial, numerofinal
    #

def filtrarnumeracion(lista):
    aux=[]
    for url in lista:
        u,i,f=obtenernumeracionpag(url)
        if f>0:
            aux.append(url)
    return aux

#Falta describir los xpath en el formulario para la noticia
#Podemos hallar elementos restantes de forma automatica obteniendo los datos de las listas



#url="https://www.eldiario.net/portal/"

#print(obtenerurls(url))
#obtenernumeracionpag("https://www.la-razon.com/nacional/")

def cargarpaginaweb(URLprincipal, urlsec):
    url=urlsec
    urlp=URLprincipal
    r=requests.get(url)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    texto=decode
    listacss=parser.xpath("//@href")
    for enlacecss in listacss:
        if not("http" in enlacecss):
            enlacenuevo='href="'+urlp+enlacecss+'"'
            #print(enlacenuevo)
            texto=texto.replace('href="'+enlacecss+'"',enlacenuevo)
    listasrc=parser.xpath("//@src")
    for enlacesrc in listasrc:
        if not("http" in enlacesrc):
            enlacenuevo='src="'+urlp+enlacesrc+'"'
            #print(enlacenuevo)
            texto=texto.replace('src="'+enlacesrc+'"',enlacenuevo)
    listasrc=parser.xpath("//@srcset")
    for enlacesrc in listasrc:
        if not("http" in enlacesrc):
            enlacenuevo='srcset="'+urlp+enlacesrc+'"'
            #print(enlacenuevo)
            texto=texto.replace('srcset="'+enlacesrc+'"',enlacenuevo)
    css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpath.css">'
    iniciobody=re.search("<body.*>",texto)
    iniciohead=re.search("<head.*>",texto)

    parte1=texto[0:iniciohead.end()]
    parte2=texto[iniciohead.end():iniciobody.end()]
    parte3=texto[iniciobody.end():]
    documento=parte1+css+parte2+parte3
    return documento

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_options.headless=True
    chrome_options.add_argument('--log-level=1')
    return chrome_options

def cargarpaginaporselenium(urlpagina):
    DRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get(urlpagina)
    print(driver.page_source)
    pagina=driver.page_source
    enlacesa=driver.find_elements(By.XPATH,"//a")

    driver.close()
    driver.quit()
    return pagina
def consultarxpathselenium(urlpagina, xpath):
    DRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(options=set_chrome_options())
    print("urlpagina selenium: ", urlpagina)
    driver.get(urlpagina)
    #print(driver.page_source)
    #pagina=driver.page_source
    enlacesa=driver.find_elements(By.XPATH,xpath)
    listaurl=[]
    listatexto=[]
    print(enlacesa)
    for enlace in enlacesa:
        print("------------------")
        print(enlace)
        url=enlace.get_attribute("href")
        texto=enlace.text
        print(url, texto)
        if not(url is None):
            listaurl.append(url)
            listatexto.append(texto)
            

    driver.close()
    driver.quit()
    return listaurl, listatexto
def sacarenlaceprin(urlprincipal):
    enlacevec=urlprincipal.split("/")
    enlace=enlacevec[0]+"//"+enlacevec[2]
    return enlace
def cargarpaginaycorregir(urlpagina, urlprin=""):
    urlp=sacarenlaceprin(urlprin)
    r=requests.get(urlpagina)
    decode=r.content.decode('utf-8')
    parser=html.fromstring(decode)
    texto=decode
    listacss=parser.xpath("//@href")
    
    for enlacecss in listacss:
        if(enlacecss=="/noticias/images/eva-copa-2404221148.jpg"):
            print("Lo encontre: ","/noticias/images/eva-copa-2404221148.jpg")
        if not("http" in enlacecss):
            enlacenuevo='href="'+urlp+enlacecss+'"'
            #print(enlacenuevo)
            texto=texto.replace('href="'+enlacecss+'"',enlacenuevo)
    listasrc=parser.xpath("//@src")
    for enlacesrc in listasrc:
        if not("http" in enlacesrc):
            enlacenuevo='src="'+urlp+enlacesrc+'"'
            print(enlacenuevo)
            print("ENLACE...",enlacesrc)
            texto=texto.replace('src="'+enlacesrc+'"',enlacenuevo)
            texto=texto.replace("src='"+enlacesrc+"'",enlacenuevo)
    listasrc=parser.xpath("//@data-src")
    for enlacesrc in listasrc:
        if not("http" in enlacesrc):
            enlacenuevo='src="'+urlp+enlacesrc+'"'
            print(enlacenuevo)
            print("ENLACE...",enlacesrc)
            texto=texto.replace('src="'+enlacesrc+'"',enlacenuevo)
            texto=texto.replace("src='"+enlacesrc+"'",enlacenuevo)	
    listasrc=parser.xpath("//@srcset")
    for enlacesrc in listasrc:
        if not("http" in enlacesrc):
            enlacenuevo='srcset="'+urlp+enlacesrc+'"'
            #print(enlacenuevo)
            texto=texto.replace('srcset="'+enlacesrc+'"',enlacenuevo)
    return texto

#print(consultarxpathselenium("http://www.elalteno.com.bo","//*[@id='block-elalteno-theme-content']/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[12]/a[1]"))
#listurl=obtenerenlaces("http://www.elalteno.com.bo","//div[3]/div/div[1]//span/div/div/div/div[2]//a")


#print(listurl)