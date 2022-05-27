
import sys, os
from pymongo import MongoClient
from datetime import date
from datetime import datetime
import time
import requests
import lxml.html as html
import json

#import enviarnotificaciones
client=MongoClient("mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority")
db = client["Noticias"]
#en caso de conectar localhost db=client["Noticia"]
colpagnot=db['Paginanoticias'] #Colleccion pagina noticias
#print(colpagnot)
listapagnot=list(colpagnot.find())
#print(listapagnot)
colnoticias=db["noticia"]


def generarfecha(texto):
    retornar=""
    try:
        dia = mes =mesnum =año = hora= ""
        intdiasem=-1
        aux=texto.replace("/", " ")
        aux=aux.replace("-", " ")
        aux=aux.replace(",", "")
        aux=aux.replace("(", " ")
        aux=aux.replace(")" ," ")
        meses=["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        mesesab=["ENE", "FEB" ,"MAR" ,"ABR" , "MAY"  ,"JUN" , "JUL" ,"AGO"  ,"SEP"  ,"OCT" ,"NOV" ,"DIC"]
        diasdelasemana=["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
        diassemab=["LU" , "MA" , "MI" , "JU", "VI"  "SA" , "DO"]
        diassema2=["LUN" , "MAR" , "MIE" , "JUE", "VIE"  "SAB" , "DOM"]
        letrastxt=aux.split()
        for dato in letrastxt:
            if(dato.isnumeric()):
                if(dia==""):
                    if(int(dato)<=31):
                        dia=dato
                    else:
                        año=dato
                elif(mes==""):
                    if(int(dato)<=12):
                        mesnum=dato
                        mes=meses[int(dato)-1]
                else:
                    año=dato
            elif dato.upper() in diasdelasemana:
                intdiasem=int(diasdelasemana.index(dato.upper()))
            elif dato.upper() in diassemab:
                intdiasem=int(diassemab.index(dato.upper()))    
            elif dato.upper() in diassema2:
                intdiasem=int(diassema2.index(dato.upper()))
            elif dato.upper() in meses :
                mesnum=meses.index(dato.upper())
                mes=meses[int(mesnum)]
                mesnum=int(mesnum)+1
            elif dato.upper() in mesesab:
                mesnum=mesesab.index(dato.upper())
                mes=meses[int(mesnum)]
                mesnum=int(mesnum)+1
            elif ":" in dato:
                hora=dato
        

        fechaencontrada=date(int(año),int(mesnum),int(dia))
        diaencontrado=fechaencontrada.weekday()
        #Si por alguna razon el dia de la semana no coincide con el dia y mes entonces el mes se convierte en dia y el dia en semana
        if diaencontrado!=intdiasem and intdiasem!=-1:
            auxdia=dia
            dia=mesnum
            mesnum=auxdia
            mes=meses[int(mesnum)-1]
        fechaencontrada=date(int(año),int(mesnum),int(dia))
        if ":" in hora:
            horaymin=hora.split(":")
            hora=horaymin[0]
            min=horaymin[1]
            retornar=datetime(int(año),int(mesnum),int(dia), int(hora), int(min))
        else:
            retornar=datetime(int(año),int(mesnum),int(dia))
    except:
        retornar="Fecha no valida"
    return retornar
            



def concatenarenlace(urlnoticia, urlprincipal):
    vecurlprin=urlprincipal.split("/")
    urlprincipal=vecurlprin[0]+"//"+vecurlprin[2]+"/"
    if str(urlprincipal[-1])=="/":
        urlprincipal=str(urlprincipal)[0:-1]
    if not("http" in str(urlnoticia)):
        urlnoticia=str(urlprincipal)+str(urlnoticia)
    return(urlnoticia)
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def esfechadehoy(textofecha):
    #Nota este algoritmo no es el mas eficiente
    #Hay que mejorarlo
    #0= no es la fecha de hoy, 1= Es la fecha de hoy, -1 fecha no valida
    retornar=0
    fechadate=generarfecha(textofecha)
    if fechadate!= "Fecha no valida":
        if fechadate.date() == datetime.today().date():
            retornar=1
    else:
        retornar=-1

    return retornar
class Noticia:
    titular=''
    resumen=''
    redactor=''
    fecha=''
    fechaasig=''
    urlimagen=''
    descripcionimagen=''
    parrafos=''
    video=''
    descripcionvideo=''
    categoriaprincipal=''
    categorias=''
    estitular=False
    fecharecup=''
    def __init__(self):
        titular=''
        resumen=''
        redactor=''
        fecha=''
        urlimagen=''
        descripcionimg=''
        parrafos=''
        video=''
        descripcionvideo=''
        categorias=''
        categoriaprincipal=''
        estitular=False
    def insertarabd(self, urlfuente):
        try:
            colnot=db.noticia
            
            consulta={
                'urlfuente':urlfuente,
                'urlnoticia':self.urlnot,
                'titular':self.titular,
                'resumen':self.resumen,
                'redactor':self.redactor,
                'fecha':self.fecha,
                'fechaasig':self.fechaasig,
                'urlimagen':self.urlimagen,
                'desimagen':self.descripcionimagen,
                'parrafos':self.parrafos,
                'video':self.descripcionvideo,
                'desvideo':self.descripcionvideo,
                'categoriaprin':self.categoriaprincipal,
                'categorias':self.categorias,
                'estiular':self.estitular,
                'fecharecup':datetime.now(),
                
            }
            colnot.insert_one(consulta)
        except:
            print("error al subir la noticia a la bd")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
                     
    def generarnotificacion(self, urlfuente):
        enviar={"urlprin":urlfuente,"url":self.urlnot, "categoria":self.categoriaprincipal, "titular":self.titular, "parrafo":self.parrafos, "imagen":self.urlimagen, "mensaje":"nueva noticia"}
        data=json.dumps(enviar)
        #enviarnotificaciones.enviarmensaje(data)
    

    def cargarnoticia(self, urlnoticia, xpaths,urlprincipal, estitular=False, categoriaprin=""):
        retornar=False
        print("URL NOTICIA: ", urlnoticia)
        if colnoticias.count_documents({"urlnoticia":urlnoticia})<1:
            self.urlnot=urlnoticia
            s = requests.Session()
            s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            s.max_redirects = 60
            
            print("urlnoticia: ",urlnoticia)
            
            rn=s.get(urlnoticia)
            tn=html.fromstring(rn.content)
            self.estitular=estitular
            self.fecharecup=datetime.now()
            if(xpaths["xpfecha"]!=""): 
                try:
                    datosfecha=tn.xpath(xpaths["xpfecha"]+"//text()")
                    print("xp fecha: ",xpaths["xpfecha"])
                    print("datosfecha: ",datosfecha)
                    fechanot=""
                    for dato in datosfecha:
                        if has_numbers(dato):
                            print
                            fechanot=fechanot+dato+" "
                    print(fechanot)
                    if(esfechadehoy(fechanot)==1):
                        #preguntamos si la fecha es detectada es la fecha de hoy
                        retornar=True #si es asi retornamos true
                        self.fechaasig=datetime.today()
                        self.fecha=fechanot
                        if(xpaths["xptitular"]!=""):
                            try:
                                self.titular=tn.xpath(xpaths["xptitular"])[0].text
                            except Exception as e:
                                self.titular=""
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                print(e)
                        #Obtenemos la categoria principal
                        self.categoriaprincipal=categoriaprin

                        if(xpaths["xpresumen"]!=""):
                            try:
                                self.resumen=tn.xpath(xpaths["xpresumen"])[0].text
                            except Exception as e:
                                self.resumen=""
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                print(e)
                        if(xpaths["xpredactor"]!=""):
                            try:
                                self.redactor=tn.xpath(xpaths["xpredactor"])[0].text
                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                self.redactor=""
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                print(e)
                        if(xpaths["xpimagen"]!=""):
                            try:
                                self.urlimagen=tn.xpath(xpaths["xpimagen"])[0].get("src")
                                if(tn.xpath(xpaths["xpimagen"])[0].get("data-srcset")!=None):
                                    self.urlimagen="https:"+str(tn.xpath(xpaths["xpimagen"])[0].get("data-srcset").split()[0])
                                if(self.urlimagen==None):
                                    self.urlimagen=tn.xpath(xpaths["xpimagen"])[0].get("href")
                                if(self.urlimagen!=None):
                                    self.urlimagen=concatenarenlace(self.urlimagen, urlprincipal)
                                print("self.urlimagen", self.urlimagen)
                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                self.urlimagen=""
                                print(exc_type, fname, exc_tb.tb_lineno)
                                print(e)
                        if(xpaths["xpdesimagen"]!=""):
                            try:
                                self.descripcionimagen=tn.xpath(xpaths["xpdesimagen"])[0].text
                            except Exception as e:
                                self.descripcionimagen=""
                                print(e)
                        if(xpaths["xpparrafos"]!=""):
                            try:
                                listaparrafos=tn.xpath(xpaths["xpparrafos"]+"//text()")
                                parr=""
                                for p in listaparrafos:
                                    parr=parr+"\n"+str(p)
                                self.parrafos=parr.replace("None","")
                            except Exception as e:
                                print(e)
                                self.parrafos=""
                        if(xpaths["xpvideo"]!=""):
                            try:
                                self.video=tn.xpath(xpaths["xpvideo"]).get("src")
                            except Exception as e:
                                print(e)
                                self.video=""
                        if(xpaths["xpdesvideo"]!=""):
                            try:
                                self.descripcionvideo=tn.xpath(xpaths["xpdesvideo"])[0].text
                            except Exception as e:
                                print(e)
                                self.descripcionvideo=""
                        if(xpaths["xpcategorias"]!=""):
                            try:
                                self.categorias=tn.xpath(xpaths["xpcategorias"])[0].text
                            except Exception as e:
                                self.categorias=""
                                print(e)
                        try:
                        
                            self.insertarabd(urlprincipal)
                            self.generarnotificacion(urlprincipal)
                        except:
                            print("problema al añadir a la bd")
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            self.numerotema=-1
                

                    else:
                        self.fecha="no valido"
                    
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(e)
            else:
                retornar=False
        else:
            print("La noticia se encuentra en la lista......")
        return retornar


def obtenerenlace(xpath, urlprincipal, textopagina):
    url=textopagina.xpath(xpath)[0].get("href")
    if not("http" in url):
        if urlprincipal[-1]=='/':
            url=urlprincipal[0:-1]+url
        else:
            url=urlprincipal+url
    return url


       


def cargarnoticias():
    colpagnot=db['Paginanoticias'] #Colleccion pagina noticias
    #print("conectando")
    listapagnot=colpagnot.find()
    #print(len(listapagnot))
    cont=0
    try:
        for pagina in listapagnot:
            cont+=1
            print("------------",cont,"---------------")
            urlprincipal=pagina["URLPrincipal"]
            if urlprincipal[-1]=="/":
                urlprincipal=urlprincipal[0:-1]
            print("urlPrincipal: ",urlprincipal)
            urls=pagina["urls"]
            idcategorias=pagina["categorias"]
            xpathrirularprin=pagina["Xpathnotprincipal"]
            xpathurlsnoticiasgral=pagina["Xpathurlsnoticias"]
            tipo=pagina["Tipo"]
            xpathsnoticia=pagina["datosnoticia"]
            #obteniendo la noticia principal de la pagina 
            if(xpathrirularprin!=""):
                r=requests.get(urlprincipal)
                t=html.fromstring(r.content)
                elemAnoticiaprincipal=t.xpath(xpathrirularprin)
                if len(elemAnoticiaprincipal)>0:
                    urlnoticiaprin=elemAnoticiaprincipal[0].get("href")
                    print("URL noticiaprincipal: ",urlnoticiaprin)
                    if not("http" in urlnoticiaprin):
                        urlnoticiaprin=urlprincipal+urlnoticiaprin
                    if colnoticias.count_documents({"urlnoticia":urlnoticiaprin})<1:
                        notprincipal=Noticia()
                        notprincipal.cargarnoticia(urlnoticiaprin,xpathsnoticia,urlprincipal,True)
                    else:
                        print("La Url ya se encuentra en la BD: ", urlnoticiaprin)
                    #recorremos la pagina segun sus secciones
                    listaurls=json.loads(urls)
                    listaidcat=json.loads(idcategorias)
                    if tipo=="nodinamica":
                        #pagina no dinamica
                        
                        for i, urlseccion in enumerate(listaurls):
                            numeronoticiassubidascat=0  
                            urlpagina=urlseccion
                            print("/*/*/*/",urls)
                            print("URLPAGINA: ",urlpagina)
                            idcat=listaidcat[i]
                            evaluar=True
                            while(numeronoticiassubidascat<15 and evaluar):
                                print("Urlpagina", urlpagina)
                                rseccion=requests.get(urlpagina)
                                tseccion=html.fromstring(rseccion.content)
                                urlsnoticias=tseccion.xpath(xpathurlsnoticiasgral)
                                print(urlsnoticias)
                                for urlnot_a in urlsnoticias:
                                    
                                    urlnot=urlnot_a.get("href")
                                    urlnot=concatenarenlace(urlnot, urlprincipal)
                                    print("url de la noticia",urlnot)
                                    print(urlnot, "num", colnoticias.count_documents({"urlnoticia":urlnot}))
                                    #Verificamos si la url no encuentra en la base de datos
                                    if colnoticias.count_documents({"urlnoticia":urlnot})<1:
                                        noti=Noticia()
                                        
                                   
                                        cargar=noti.cargarnoticia(urlnot,xpathsnoticia, urlprincipal, categoriaprin=idcat)
                                        print("datos cargar: ",cargar)
                                        if cargar==False:
                                            print("Se detendra la categoria....")
                                            evaluar=False  #La busqueda de paginacion se detiene cuando no hay noticias con la fecha de hoy
                                            break
                                        numeronoticiassubidascat+=1
                                        print("n: ",numeronoticiassubidascat)
                                    else:
                                        consulta=colnoticias.find_one({"urlnoticia":urlnot})
                                        print("elemento",consulta)
                                        if(consulta["estiular"]==False):
                                            print("Esta noticia ya esta en la lista")
                                            print(urlnot)
                                            evaluar=False
                                            break
                                    
                                try:
                                    paginasig=obtenerenlace(pagina["Xpathpagsig"],urlprincipal,tseccion)
                                    if(paginasig != "" and evaluar==True):
                                        print("Obteniendo pagina siguiente")
                                        urlpagina=paginasig
                                        print("urlsig= ",urlpagina)
                                        
                                except:
                                    evaluar=False

                    else:
                        print("Pagina dinamica.....")
                        for i, urlseccion in enumerate(listaurls):
                            idcat=listaidcat[i]
                            listaurlsnot=pagdimcargarnoticias(urlseccion,xpathurlsnoticiasgral,pagina["Xpathpagsig"])
                            for urlnoticia in listaurlsnot:
                                noti=Noticia()
                                urlnoticia=concatenarenlace(urlnoticia, urlprincipal)
                                if colnoticias.count_documents({"urlnoticia":urlnot})<1:
                                    cargar=noti.cargarnoticia(urlnoticia,xpathsnoticia, urlprincipal, categoriaprin=idcat)
                                    if(cargar==False):
                                        print("Se detendra la categoria")
                                        break
                                else:
                                    #En caso de que la noticia sea titular seguimos analizando
                                    consulta=colnoticias.find_one({"urlnoticia":urlnot})
                                    print("elemento",consulta)
                                    if(consulta["estiular"]==False):
                                        print("Esta noticia ya esta en la lista")
                                        evaluar=False
                                        break
    except Exception as e:
        print("Fallo al cargar la pagina")
        print(pagina)
        print(e)








#Paginas dinamicas
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
"""
def  load_driver():
	options = webdriver.FirefoxOptions()
	# enable trace level for debugging 
	options.log.level = "trace"
	options.add_argument("-remote-debugging-port=9224")
	options.add_argument("-headless")
	options.add_argument("-disable-gpu")
	options.add_argument("-no-sandbox")

	binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

	firefox_driver = webdriver.Firefox(
		firefox_binary=binary,
		executable_path=os.environ.get('GECKODRIVER_PATH'),
		options=options)

	return firefox_driver
"""       
def set_firefox_options():
    options = Options()
    options.add_argument("-no-sandbox")
    options.add_argument("--headless")
    options.binary_location = r'/app/vendor/firefox/firefox'
    return options

def pagdimcargarnoticias(url, xpath, xpathboton):
    print("urld ", url)
    print("xpath ", xpath)
    print("xpathboton ", xpathboton)
    #binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    driver = driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=set_firefox_options())
    driver.get(url)
    if xpathboton!="":
        try:
            botonvermas=driver.find_element(By.XPATH,xpathboton)
            driver.execute_script("arguments[0].click();", botonvermas) #Hacemos click en el boton ver mas
            time.sleep(7)
            driver.execute_script("arguments[0].click();", botonvermas) #Hacemos click en el boton ver mas
            time.sleep(7)
        except Exception as e:
            print(e)
            print("No se pudo cargar mas noticias")
    print("consultandoxpath")
    listaelementos=driver.find_elements(By.XPATH,xpath)
    #print(driver.page_source)
    listaurls=[]
    for elemento in listaelementos:
        print(elemento)
        listaurls.append(elemento.get_attribute("href"))
        print(elemento.get_attribute("href"))
    driver.close()
    driver.quit()
    return(listaurls)

def cargarnoticiasdeunapagina(urlpagina):
    colpagnot=db['Paginanoticias'] #Colleccion pagina noticias
    pagina=colpagnot.find_one({"URLPrincipal":urlpagina})
    urlprincipal=pagina["URLPrincipal"]
    if urlprincipal[-1]=="/":
        urlprincipal=urlprincipal[0:-1]
    print("urlPrincipal: ",urlprincipal)
    urls=pagina["urls"]
    idcategorias=pagina["categorias"]
    xpathrirularprin=pagina["Xpathnotprincipal"]
    xpathurlsnoticiasgral=pagina["Xpathurlsnoticias"]
    tipo=pagina["Tipo"]
    xpathsnoticia=pagina["datosnoticia"]
    #obteniendo la noticia principal de la pagina 
    print(xpathrirularprin)
    if(xpathrirularprin!=""):
        r=requests.get(urlprincipal)
        t=html.fromstring(r.content)
        elemAnoticiaprincipal=t.xpath(xpathrirularprin)
        print(elemAnoticiaprincipal)
        if len(elemAnoticiaprincipal)>0:
            urlnoticiaprin=elemAnoticiaprincipal[0].get("href")
            print("URL noticiaprincipal: ",urlnoticiaprin)
            if not("http" in urlnoticiaprin):
                urlnoticiaprin=urlprincipal+urlnoticiaprin
            if colnoticias.count_documents({"urlnoticia":urlnoticiaprin})<1:
                notprincipal=Noticia()
                notprincipal.cargarnoticia(urlnoticiaprin,xpathsnoticia,urlprincipal,True)
            else:
                print("La Url ya se encuentra en la BD: ", urlnoticiaprin)
            #recorremos la pagina segun sus secciones
            listaurls=json.loads(urls)
            listaidcat=json.loads(idcategorias)
            if tipo=="nodinamica":
                #pagina no dinamica
                
                for i, urlseccion in enumerate(listaurls):
                    numeronoticiassubidascat=0  
                    urlpagina=urlseccion
                    print("/*/*/*/",urls)
                    print("URLPAGINA: ",urlpagina)
                    idcat=listaidcat[i]
                    evaluar=True
                    while(numeronoticiassubidascat<15 and evaluar):
                        print("Urlpagina", urlpagina)
                        rseccion=requests.get(urlpagina)
                        tseccion=html.fromstring(rseccion.content)
                        urlsnoticias=tseccion.xpath(xpathurlsnoticiasgral)
                        print(urlsnoticias)
                        for urlnot_a in urlsnoticias:
                            
                            urlnot=urlnot_a.get("href")
                            urlnot=concatenarenlace(urlnot, urlprincipal)
                            print("url de la noticia",urlnot)
                            print(urlnot, "num", colnoticias.count_documents({"urlnoticia":urlnot}))
                            #Verificamos si la url no encuentra en la base de datos
                            if colnoticias.count_documents({"urlnoticia":urlnot})<1:
                                noti=Noticia()
                                
                            
                                cargar=noti.cargarnoticia(urlnot,xpathsnoticia, urlprincipal, categoriaprin=idcat)
                                print("datos cargar: ",cargar)
                                if cargar==False:
                                    print("Se detendra la categoria....")
                                    evaluar=False  #La busqueda de paginacion se detiene cuando no hay noticias con la fecha de hoy
                                    break
                                numeronoticiassubidascat+=1
                                print("n: ",numeronoticiassubidascat)
                            else:
                                consulta=colnoticias.find_one({"urlnoticia":urlnot})
                                print("elemento",consulta)
                                if(consulta["estiular"]==False):
                                    print("Esta noticia ya esta en la lista")
                                    print(urlnot)
                                    evaluar=False
                                    break
                            
                        try:
                            paginasig=obtenerenlace(pagina["Xpathpagsig"],urlprincipal,tseccion)
                            if(paginasig != "" and evaluar==True):
                                print("Obteniendo pagina siguiente")
                                urlpagina=paginasig
                                print("urlsig= ",urlpagina)
                                
                        except:
                            evaluar=False

            else:
                print("Pagina dinamica.....")
                for i, urlseccion in enumerate(listaurls):
                    idcat=listaidcat[i]
                    listaurlsnot=pagdimcargarnoticias(urlseccion,xpathurlsnoticiasgral,pagina["Xpathpagsig"])
                    for urlnoticia in listaurlsnot:
                        noti=Noticia()
                        urlnoticia=concatenarenlace(urlnoticia, urlprincipal)
                        if colnoticias.count_documents({"urlnoticia":urlnoticia})<1:
                            cargar=noti.cargarnoticia(urlnoticia,xpathsnoticia, urlprincipal, categoriaprin=idcat)
                            if(cargar==False):
                                print("Se detendra la categoria")
                                break
                        else:
                            #En caso de que la noticia sea titular seguimos analizando
                            consulta=colnoticias.find_one({"urlnoticia":urlnoticia})
                            print("elemento",consulta)
                            if(consulta["estiular"]==False):
                                print("Esta noticia ya esta en la lista")
                                evaluar=False
                                break
def probarcargarnoticia(urlnoticia, urlfuente):
    colfuente=colpagnot.find_one({"URLPrincipal":urlfuente})
    rn=requests.get(urlnoticia)
    tn=html.fromstring(rn.content)
    listaxpath=colfuente["datosnoticia"]
    print(listaxpath["xpimagen"])
    urlimg=tn.xpath(listaxpath["xpimagen"])
    print(str(urlimg[0].get("data-srcset")).split())

def cargartodaslaspaginas():
    while True:
        print("cargando")
        cargarnoticias()
        time.sleep(30)

#cargartodaslaspaginas()
#cargarnoticiasdeunapagina("https://paginasiete.bo/")
#probarcargarnoticia("https://paginasiete.bo/portada/muere-sergio-perovic-esposo-de-la-exalcaldesa-angelica-sosa-AA2626561","https://paginasiete.bo/")
#prueba()

#arrayaños=["1 de abril de 2022","01/04/2022","01-04-2022","04-01-2022","1 de abril 2022","2020-04-01","abril 01 2022","abril 1 2022","abril 01 de 2022","2022 abril 01", "viernes, abril 1, 2022", "miércoles, 6 de abril de 2022 · 15:01", "Lunes, 28 de Marzo del 2022", "11:24 ET(15:24 GMT) 7 Abril, 2022", "abril 7, 2022","marzo 11, 2022","Jue, 04/07/2022 - 08:20", "07 Abr 2022","<!--//--><![CDATA[//><!-- if(window.da2a)da2a.script_load(); //--><!]]>"]


#Stringfecha="  / 4 de abril de 2022  / 01:37"
#esfechadehoy(Stringfecha)

