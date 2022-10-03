from multiprocessing.connection import wait
from ntpath import join
from requestshtml import AsyncHTMLSession
from requestshtml import HTMLSession
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from datetime import date
from datetime import datetime
import asyncio
import enviarnotificaciones
import pytz
from unsync import unsync
client=MongoClient("mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority")
db = client["Noticias"]

def editarultimarevision(urlprin):
    db.paginanoticia.update_one({'url': urlprin},{"$set":{
			"ultimarevision":datetime.now(pytz.timezone('Etc/GMT+4'))
			}})
def generarnotificacion( enviar):
        enviar["mensaje"]="nueva noticia"
        data=json.dumps(enviar, indent=4, sort_keys=True, default=str)
        enviarnotificaciones.enviarmensaje(data)
def añadirnoticia(noticia):
    if not urlnoticiaexiste(noticia["urlnoticia"]):
        if noticia["urlnoticia"]!="" and noticia["titular"]!="" and noticia["titular"]!="\n":
            db["noticia"].insert_one(noticia)
            generarnotificacion(noticia)
            print("Noticia añadida")
        else:
            print("Ocurrio un problema al momento de añadir la noticia")
    else:
        print("Men: La noticia se encuentra en la base de datos")

def urlnoticiaexiste(urlnot):
    notenc=db.noticia.find_one({"urlnoticia":urlnot})
    if notenc==None:
        return False
    else:
        return True
def obtenerdominioprincipal(url):
    arrurl=url.split("/")
    protocolo=arrurl[0]
    dom=arrurl[2]
    return protocolo+"://"+dom
def autocompletarurl(url, urlprincipal):
    retonar=url
    if url != "":
        arrayurlprin=urlprincipal.split("/")
        domprin= arrayurlprin[2]
        protocolo= arrayurlprin[0]
        if not domprin in url:
            retonar=protocolo+"://"+domprin+url
    return retonar
def atributoenxpath(xpath):
    retornar=False
    posfin=str(xpath).rfind("/")
    ultimoel=xpath[posfin:]
    if("/@" in ultimoel or "/text()" in ultimoel):
        retornar=True
    return retornar
def recolectarnoticia(url, regla, noticia={}):
    #Este algoritmo se encarga de recolectar noticias mediante reglas o parametros xpath

    try:
        session = HTMLSession() 
        pagina = session.get(url)
        try:
            #Cargando scripts de la pagina
           pagina.html.render(sleep = 10, timeout=50)
        except:
            print("no se pudo completar la carga de la pagina")
        #cargando titular de la notica
        try:
            if (regla.get("xptitular")!="" or regla.get("xptitular")!=None):
                titular=""
                if atributoenxpath(regla["xptitular"]):
                    titular=pagina.html.xpath(regla["xptitular"],first=True)
                else:
                    titular=pagina.html.xpath(regla["xptitular"]+"/text()",first=True)
                if titular!="" and titular != None:
                    noticia["titular"]=titular
        except:
            print("No se pudo cargar el titular, existe un problema con el xpath: ",regla.get("xptitular"))
        #cargando resumen de la notica
        try:
            if (regla.get("xpresumen")!="" or regla.get("xpresumen")!=None):
                resumen=""
                if atributoenxpath(regla["xpresumen"]):
                    resumen=pagina.html.xpath(regla["xpresumen"],first=True)
                else:
                    resumen=pagina.html.xpath(regla["xpresumen"]+"/text()",first=True)
                if resumen !="" and resumen !=None:
                    noticia["resumen"]=resumen
        except:
            print("No se pudo cargar el resumen, existe un problema con el xpath: ",regla.get("xpresumen"))
        #cargando imagen
        try:
            if (regla.get("xpimg")!="" or regla.get("xpimg")!=None):
                urlimagen=""
                if atributoenxpath(regla["xpimg"]):
                    urlimagen=pagina.html.xpath(regla["xpimg"],first=True)
                else:
                    urlimagen=pagina.html.xpath(regla["xpimg"]+"/@src",first=True)
                if urlimagen!="" and urlimagen != None:
                    noticia["urlimagen"]=urlimagen
                    noticia["urlimagen"]=noticia["urlimagen"].split(" ")[0]
                    noticia["urlimagen"]=autocompletarurl(noticia["urlimagen"],url)

        except:
            print("No se pudo cargar el la imagen, existe un problema con el xpath: ",regla.get("xpimg"))
        #cargando descripcion de la imagen
        try:
            if (regla.get("xpdesimg")!="" or regla.get("xpdesimg")!=None):
                desimg=""
                if atributoenxpath(regla["xpdesimg"]):
                    desimg=pagina.html.xpath(regla["xpdesimg"],first=True)
                else:
                    desimg=pagina.html.xpath(regla["xpdesimg"]+"/text()",first=True)
                if desimg!="" and desimg!=None:
                    noticia["desimg"]=desimg
        except:
            print("No se pudo cargar la descpricion de la imagen, existe un problema con el xpath: ",regla.get("xpimg"))
        #cargando descripcion de la imagen
        try:
            if (regla.get("xpredactor")!="" or regla.get("xpredactor")!=None):
                redactor=""
                if atributoenxpath(regla["xpredactor"]):
                    redactor=pagina.html.xpath(regla["xpredactor"], first=True)
                else:
                    redactor=pagina.html.xpath(regla["xpredactor"]+"/text()", first=True)
                if redactor!="" and redactor!= None:
                    noticia["redactor"]=redactor
        except:
            print("No se pudo cargar el redactor, existe un problema con el xpath: ",regla.get("xpredactor"))
        #cargando fecha
        try:
            if (regla.get("xpfecha")!="" or regla.get("xpfecha")!=None):
                fecha=""
                if atributoenxpath(regla["xpfecha"]):
                    fecha=pagina.html.xpath(regla["xpfecha"], first=True)
                else:
                    fecha=pagina.html.xpath(regla["xpfecha"]+"/text()", first=True)
                if fecha != "" and fecha != None:
                    noticia["fecha"]=fecha
        except:
            print("No se pudo cargar la fecha, existe un problema con el xpath: ",regla.get("xpfecha"))
        #cargando parrafos
        try:
            if (regla.get("xpparrafos")!="" or regla.get("xpparrafos")!=None):
                parrafos=""
                if atributoenxpath(regla["xpparrafos"]):
                    parrafos=pagina.html.xpath(regla["xpparrafos"])
                else:
                    parrafos=pagina.html.xpath(regla["xpparrafos"]+"/text()")
                noticia["parrafos"]='\n'.join(parrafos)
        except:
            print("No se pudo cargar los parrafos de la noticia, existe un problema con el xpath:  ",regla.get("xpparrafos"))
        try:
            if (regla.get("xphashtags")!="" or regla.get("xphashtags")!=None):
                    if atributoenxpath(regla["xphashtags"]):
                        noticia["hashtags"]=pagina.html.xpath(regla["xphashtags"])
                    else:
                        noticia["hashtags"]=pagina.html.xpath(regla["xphashtags"]+"/text()")
        except:
            print("No se pudo cargar los hashtags, existe un problema con el xpath: ",regla.get("xphashtags"))
        pagina.close()
        try:
            session.close()
        except:
            print("No se pudo cerrar session")
    except:
        print("URL no valida: ",url)
    return noticia

@unsync
async def recolectarnoticiasmultiple(url, regla, idcategoria=""):
    #Este algoritmo se encarga de recolectar noticias mediante reglas o parametros xpath
   
    #contador en caso de que se encuentren noticias repetidas
    listaurls=[]
    listatitulares=[]
    listafecha=[]
    listaimg=[]
    listaredactor=[]
    listadescripcion=[]
    print("//////////////////////////////")
    print(url)
    print("cargando...")
    try:
        urlfuente=obtenerdominioprincipal(url)
        asession = AsyncHTMLSession() 
        pagina = await asession.get(url)
        try:
            #Cargando scripts de la pagina
            await pagina.html.arender(sleep = 10, timeout=50)
        except:
            print("no se pudo completar la carga de la pagina")
        #Cargando las urls de las noticias
        try:
            if (regla.get("xpathurl")!="" or regla.get("xpathurl")!=None):
                if atributoenxpath(regla["xpathurl"]):
                    listaurls=pagina.html.xpath(regla["xpathurl"])
                else:
                    listaurls=pagina.html.xpath(regla["xpathurl"]+"/@href")
        except:
            print("No se pudo cargar las URLs, existe un problema con el xpath: ",regla.get("xpathurl"))
        #cargando titular de la notica
        try:
            if (regla.get("xpathtitular")!="" or regla.get("xpathtitular")!=None):
                if atributoenxpath(regla["xpathtitular"]):
                    listatitulares=pagina.html.xpath(regla["xpathtitular"])
                else:
                    listatitulares=pagina.html.xpath(regla["xpathtitular"]+"/text()")
        except:
            print("No se pudo cargar los titulares, existe un problema con el xpath: ",regla.get("xpathtitular"))
        #cargando fecha
        try:
            if (regla.get("xpathfecha")!="" or regla.get("xpathfecha")!=None):
                if atributoenxpath(regla["xpathfecha"]):
                    listafecha=pagina.html.xpath(regla["xpathfecha"])
                else:
                    listafecha=pagina.html.xpath(regla["xpathfecha"]+"/text()")
        except:
            print("No se pudo cargar las fechas de la categoria, existe un problema con el xpath: ",regla.get("xpathfecha"))
        #cargando imagen
        try:
            if (regla.get("xpathimg")!="" or regla.get("xpathimg")!=None):
                if atributoenxpath(regla["xpathimg"]):
                    listaimg=pagina.html.xpath(regla["xpathimg"])
                else:
                    listaimg=pagina.html.xpath(regla["xpathimg"]+"/@src")
        except:
            print("No se pudo cargar el las imagenes, existe un problema con el xpath: ",regla.get("xpathimg"))
        #cargando redactor de la imagen
        try:
            if (regla.get("xpathredactor")!="" or regla.get("xpathredactor")!=None):
                if atributoenxpath(regla["xpathredactor"]):
                    listaredactor=pagina.html.xpath(regla["xpathredactor"])
                else:
                    listaredactor=pagina.html.xpath(regla["xpathredactor"]+"/text()")
        except:
            print("No se pudo cargar el redactor, existe un problema con el xpath: ",regla.get("xpathredactor"))

        #cargando descripciones
        try:
            if (regla.get("xpathdescripcion")!="" or regla.get("xpathdescripcion")!=None):
                if atributoenxpath(regla["xpathdescripcion"]):
                    listadescripcion=pagina.html.xpath(regla["xpathdescripcion"])
                else:
                    listadescripcion=pagina.html.xpath(regla["xpathdescripcion"]+"/text()")
        except:
            print("No se pudo cargar los parrafos de la noticia, existe un problema con el xpath:  ",regla.get("xpathdescripcion"))

        pagina.close()
        try:
            await asession.close()
        except:
            print("No se pudo cerrar session")
        conturls=0
        for urlnot in listaurls:
            print("------------")
            print("url:", urlnot)
            #preguntamos si la url existe en la base de datos
            if not urlnoticiaexiste(urlnot):
                titular=""
                urlimagen=""
                fecha=""
                redactor=""
                descripcion=""
                if len(listatitulares)>conturls:
                    titular=listatitulares[conturls]
                if len(listafecha)>conturls:
                    fecha=listafecha[conturls]
                if len(listaimg)>conturls:
                    urlimagen=listaimg[conturls]
                if len(listaredactor)>conturls:
                    redactor=listaredactor[conturls]
                if len(listadescripcion)>conturls:
                    descripcion=listadescripcion[conturls]
                noticia={
                    "urlfuente":urlfuente,
                    "categoria":idcategoria,
                    "estitular":False,
                    "urlnoticia":urlnot,
                    "titular":titular,
                    "resumen":descripcion,
                    "redactor":redactor,
                    "fecha":fecha,
                    "fechaasig":datetime.now(pytz.timezone('Etc/GMT+4')),
                    "urlimagen":urlimagen,
                    "desimagen":"",
                    "parrafos":"",
                    "hashtags":""

                }
                if regla.get("reglainterna")!="" or regla.get("reglainterna")!=None:
                    noticia=recolectarnoticia(urlnot,regla["reglainterna"],noticia)
                print("Titular: ",noticia["titular"])
                print("fecha; ", noticia["fecha"])
                print("parrafos: ",str(noticia["parrafos"])[0:100],"...")
                print("urlimagen: ", noticia["urlimagen"])
                añadirnoticia(noticia)
            else:
                print("La URL se encuentra en la Base de datos")
    except:
        print("URL no valida")


@unsync
async def recolectarportada(url, regla):
    #Este algoritmo se encarga de recolectar las noticias de portada
    #contador en caso de que se encuentren noticias repetidas
    
    print("//////////////////////////////")
    print(url)
    print("cargando...")
    try:
        urlfuente=obtenerdominioprincipal(url)
        asession = AsyncHTMLSession() 
        pagina = await asession.get(url)
        try:
            #Cargando scripts de la pagina
            await pagina.html.arender(sleep = 10, timeout=50)
        except:
            print("no se pudo completar la carga de la pagina")
        noticia={
                    "urlfuente":urlfuente,
                    "categoria":"",
                    "estitular":False,
                    "urlnoticia":"",
                    "titular":"",
                    "resumen":"",
                    "redactor":"",
                    "fecha":"",
                    "fechaasig":datetime.now(pytz.timezone('Etc/GMT+4')),
                    "urlimagen":"",
                    "desimagen":"",
                    "parrafos":"",
                    "hashtags":""

                }
        #Cargando las urls de las noticias
        try:
            if (regla.get("xpathurl")!="" or regla.get("xpathurl")!=None):
                if atributoenxpath(regla["xpathurl"]):
                    noticia["urlnoticia"]=pagina.html.xpath(regla["xpathurl"], first=True)
                else:
                    noticia["urlnoticia"]=pagina.html.xpath(regla["xpathurl"]+"/@href",first=True)
        except:
            print("No se pudo cargar las URLs, existe un problema con el xpath: ",regla.get("xpathurl"))
        #cargando titular de la notica
        try:
            if (regla.get("xpathtitular")!="" or regla.get("xpathtitular")!=None):
                if atributoenxpath(regla["xpathtitular"]):
                    noticia["titular"]=pagina.html.xpath(regla["xpathtitular"],first=True)
                else:
                    noticia["titular"]=pagina.html.xpath(regla["xpathtitular"]+"/text()",first=True)
        except:
            print("No se pudo cargar los titulares, existe un problema con el xpath: ",regla.get("xpathtitular"))
        #cargando fecha
        try:
            if (regla.get("xpathfecha")!="" or regla.get("xpathfecha")!=None):
                if atributoenxpath(regla["xpathfecha"]):
                    noticia["fecha"]=pagina.html.xpath(regla["xpathfecha"], first=True)
                else:
                    noticia["fecha"]=pagina.html.xpath(regla["xpathfecha"]+"/text()", first=True)
        except:
            print("No se pudo cargar las fechas de la categoria, existe un problema con el xpath: ",regla.get("xpathfecha"))
        #cargando imagen
        try:
            if (regla.get("xpathimg")!="" or regla.get("xpathimg")!=None):
                if atributoenxpath(regla["xpathimg"]):
                    noticia["urlimagen"]=pagina.html.xpath(regla["xpathimg"], first=True)
                else:
                    noticia["urlimagen"]=pagina.html.xpath(regla["xpathimg"]+"/@src", first=True)
        except:
            print("No se pudo cargar el las imagenes, existe un problema con el xpath: ",regla.get("xpathimg"))
        #cargando redactor de la imagen
        try:
            if (regla.get("xpathredactor")!="" or regla.get("xpathredactor")!=None):
                if atributoenxpath(regla["xpathredactor"]):
                    noticia["redactor"]=pagina.html.xpath(regla["xpathredactor"], first=True)
                else:
                    noticia["redactor"]=pagina.html.xpath(regla["xpathredactor"]+"/text()", first=True)
        except:
            print("No se pudo cargar el redactor, existe un problema con el xpath: ",regla.get("xpathredactor"))

        #cargando descripciones
        try:
            if (regla.get("xpathdescripcion")!="" or regla.get("xpathdescripcion")!=None):
                if atributoenxpath(regla["xpathdescripcion"]):
                    noticia["resumen"]=pagina.html.xpath(regla["xpathdescripcion"], first=True)
                else:
                    noticia["resumen"]=pagina.html.xpath(regla["xpathdescripcion"]+"/text()", first=True)
        except:
            print("No se pudo cargar la descripcion de la noticia, existe un problema con el xpath:  ",regla.get("xpathdescripcion"))

        pagina.close()
        try:
            await asession.close()
        except:
            print("No se pudo cerrar session")
        print("------------")
        print("url:", noticia["urlnoticia"])
        #preguntamos si la url existe en la base de datos
        if not urlnoticiaexiste(noticia["urlnoticia"]):
            if regla.get("reglainterna")!="" or regla.get("reglainterna")!=None:
                noticia=recolectarnoticia(noticia["urlnoticia"],regla["reglainterna"],noticia)
            print("Titular: ",noticia["titular"])
            print("fecha; ", noticia["fecha"])
            print("parrafos: ",str(noticia["parrafos"])[0:100],"...")
            print("urlimagen: ", noticia["urlimagen"])
            añadirnoticia(noticia)
        else:
            print("La URL se encuentra en la Base de datos")
    except:
        print("URL no valida")

def monitorearnoticias():
    while(True):
        paginanoticia=db.paginanoticia.find_one({},sort=[('ultimarevision', 1)])
        print("-----------------",paginanoticia["url"],"----------------")
        editarultimarevision(paginanoticia["url"])
        print("Añadiendo noticias de portada...")
        portadas=paginanoticia["portada"]
        for port in portadas:
            urlport=port["urlportada"]
            reglaport=db.Reglas.find_one({"_id":ObjectId(str(port["idregla"]))})
            recolectarportada(urlport,reglaport)
        categorias=paginanoticia["categorias"]
        for cat in categorias:
            urlcat=cat["url"]
            print("url: ",urlcat)
            idcat=cat["idcategoria"]
            reglacat=db.Reglas.find_one({"_id":ObjectId(str(cat["idregla"]))})
            recolectarnoticiasmultiple(urlcat,reglacat,idcat)
"""
#prueba monitorear noticia
urlnot="https://www.la-razon.com/santa-cruz/2022/08/01/rector-de-la-uagrm-propone-suspender-el-paro-civico-de-48-horas-en-santa-cruz/"
reglas={"xptitular": "//*[@id='lr-main']/div[1]//h1[1]",
    "xpimg": "//*[@id='lr-main']/div[1]//img[1]",
    "xpparrafos": "//*[@id='lr-main']/div[1]//div[3]/p",
    }

noticia={
    "titular":"No se cambiara el titular",
    "parrafos":""
}

print("/*/*/*/*/")
noticia=recolectarnoticia(urlnot, reglas,noticia).result()
print(noticia)
"""

#prueba monitorear categoria
regla={
  "xpathurl": "//*[@id='lr-main']/div/div/div/div/div/div//div[2]/a",
  "xpathtitular": "esto no es un xpath",
  "xpathfecha": "//*[@id='lr-main']//span[4]/a[1]",
  "xpathimg": "//*[@id='lr-main']/div/div/a[1]",
  "xpathredactor": "//*[@id='lr-main']//span[2]/a",
  "xpathdescripcion": "//*[@id='lr-main']//div[2]/p[1]",
  "reglainterna": {
    "xptitular": "//*[@id='lr-main']/div[1]//h1[1]",
    "xpresumen": "//*[@id='lr-main']/div[1]/div/div[1]/div[1]/div[1]//p[1]",
    "xpimg": "//*[@id='lr-main']/div[1]//img[1]",
    "xpdesimg": "//*[@id='lr-main']/div[1]//div[2]//p[2]"  }
}


#recolectarnoticiasmultiple("https://www.la-razon.com/nacional/",regla, "").result()

"""
#Actualizando las revisiones
listapagnot=db.paginanoticia.find({})
import time
for pag in listapagnot:
    editarultimarevision(pag["url"])
    time.sleep(1)"""

#monitorearnoticias()