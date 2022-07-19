
from email.mime import image
from requestshtml import AsyncHTMLSession
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from datetime import date
from datetime import datetime
import asyncio
import enviarnotificaciones
from unsync import unsync
client=MongoClient("mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority")
db = client["Noticias"]
def generarnotificacion( enviar):
        enviar["mensaje"]="nueva noticia"
        data=json.dumps(enviar, indent=4, sort_keys=True, default=str)
        enviarnotificaciones.enviarmensaje(data)
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
@unsync
async def consultarportada(urlprincipal,urlportada, idreglap):
    print("inicio portada..............")
    print("idregla: ",str(idreglap))
    reglaportada=db["Reglas"].find_one({"_id":ObjectId(str(idreglap))})
    asession = AsyncHTMLSession() 
    r = await asession.get(urlportada)
    try:
        await r.html.arender(sleep = 10, timeout=50)
    except:
        print("no se pudo completar la carga de la pagina")
    urlnoticiaportada=""
    titularportada=""
    fecha=""
    imagen=""
    redactor=""
    descripcion=""
    parrafos=""
    desimagen=""

    #consultamos diversos xpath
    print("reglaportada: ",reglaportada)
    #print("xpathurl: ",reglaportada["xpathurl"])
    try:
        urlnoticiaportada=r.html.xpath(reglaportada["xpathurl"]+"/@href")[0]
        if not("http" in urlnoticiaportada and urlnoticiaportada!=""):
            urlnoticiaportada=urlprincipal+urlnoticiaportada
    except(Exception):
        print("error al cargar url")
    try:
        titularportada=r.html.xpath(reglaportada["xpathtitular"]+"/text()")[0]
    except(Exception):
        print("error al cargar titular")
    try:
        listfecha=r.html.xpath(reglaportada["xpathfecha"]+"/text()")
        for f in listfecha:
            fecha=fecha+f
    except(Exception):
        print("error al cargar fecha")
    try:
        imagen=r.html.xpath(reglaportada["xpathimg"]+"/@data-srcset")[0]
    except(Exception):
        print("error al cargar imagen (srcset)")
        print(Exception)
    try:
        if imagen=="" or imagen==None: 
            imagen=r.html.xpath(reglaportada["xpathimg"]+"/@src")[0]
            if not urlprincipal in imagen:
                imagen=urlprincipal+imagen
    except(Exception):
        print("error al cargar imagen (src)")
        print(Exception)
    try:
        if imagen=="" or imagen==None: 
            imagen=r.html.xpath(reglaportada["xpathimg"]+"/@href")[0]
            if not urlprincipal in imagen:
                imagen=urlprincipal+imagen
    except(Exception):
        print("error al cargar imagen (href)")
        print(Exception)
    try:
        redactor=r.html.xpath(reglaportada["xpathredactor"]+"/text()")[0]
    except(Exception):
        print("error al cargar redactor")
    try:
        descripcion=r.html.xpath(reglaportada["xpathdescripcion"]+"/text()")[0]
    except(Exception):
        print("error al cargar descripcion")
    print("tiporegla",reglaportada["tiporegla"])
    reglainterna=reglaportada["reglainterna"]
    
    noticia={
        "urlfuente":urlprincipal,
        "urlnoticia":urlnoticiaportada,
        "titular":titularportada,
        "estitular":True,
        "resumen":descripcion,
        "redactor":redactor,
        "fecha":fecha,
        "fecharecup":datetime.today(),
        "urlimagen":imagen,
        "categoriaprin":"",
        "parrafos":"",
        "desimagen":"",
        "hashtags":""
    }
    urlimagenint=""
    cantidadnot=len(list(db["noticia"].find({"urlnoticia":urlnoticiaportada})))
    if reglainterna!="" and urlnoticiaportada!="" and cantidadnot==0:
        r2 = await asession.get(urlnoticiaportada)
        titularint=r2.html.xpath(reglainterna["xptitular"]+"/text()")[0]
        if titularint!="" and noticia["titular"]=="":
            noticia["titular"]=titularint
        try:
            resumen=r2.html.xpath(reglainterna["xpresumen"]+"/text()")[0]
            if resumen!="":
                noticia["resumen"]=resumen
        except(Exception):
            print("error al cargar resumen interno")
        try:
            urlimagenint=r2.html.xpath(reglainterna["xpimg"]+"/@data-srcset")[0]
        except(Exception):
            print("error al cargar imagen (data srcset")
            print(Exception)
        try:
            if urlimagenint=="" or urlimagenint==None: 
                urlimagenint=r2.html.xpath(reglainterna["xpimg"]+"/@src")[0]
        except(Exception):
            print("error al cargar imagen (src)")
            print(Exception)
        try:
            if urlimagenint=="" or urlimagenint==None: 
                urlimagenint=r2.html.xpath(reglainterna["xpimg"]+"/@href")[0]
        except(Exception):
            print("error al cargar imagen (href)")
            print(Exception)
        if urlimagenint!="" and noticia["urlimagen"]=="":
            noticia["urlimagen"]=urlimagenint
        try:
            desimagen=r2.html.xpath(reglainterna["xpdesimg"]+"/text()")[0]
            noticia["desimagen"]=desimagen
        except(Exception):
            print("error al cargar descripcion img int")
            print(Exception)
        try:
            redactor=r2.html.xpath(reglainterna["xpredactor"]+"/text()")[0]
            if redactor!="" and noticia["redactor"]=="":
                noticia["redactor"]=redactor
        except(Exception):
            print("error al cargar redactor interno")
        try:
            fechaint=""
            listfechaint=r2.html.xpath(reglainterna["xpfecha"]+"/text()")
            for fe in listfechaint:
                fechaint=fechaint+fe
            if(generarfecha(fechaint)!="Fecha no valida"):
                noticia["fecha"]=fechaint
        except(Exception):
            print("error al cargar fecha interna")
        
        listaparrafos=r2.html.xpath(reglainterna["xpparrafos"]+"/text()")
        for p in listaparrafos:
            parrafos=parrafos+p
        noticia["parrafos"]=parrafos
        
        try:
            hashtags=r2.html.xpath(reglainterna["xpresumen"]+"/text()")
            noticia["hashtags"]=hashtags
        except(Exception):
            print("error al cargar hashtags int")
        r2.close()
    r.close()
    try:
        await asession.close()
    except:
        print("No se pudo cerrar session")
    añadirnoticia(noticia)
    print("fin portada")
    return noticia
@unsync
async def monitorearcat(urlprincipal,urlcategoria,categoria ,idreglascategoria):
    #print("idregla: ",idreglap)
    reglascategoria=db["Reglas"].find_one({"_id": ObjectId(str(idreglascategoria))})
    #print("idreglascat",idreglascategoria)
    #print("reglascategoria", reglascategoria)
    asession = AsyncHTMLSession()
    r = await asession.get(urlcategoria)
    """
    try:
        await r.html.arender(sleep = 10, timeout=50)
    except:
        print("no se pudo completar la carga de la pagina")
    """
    listaurls=[]
    try:
        listaurls=r.html.xpath(reglascategoria["xpathurl"]+"/@href")
    except:
        print("Error en url")
    try:
        listastitulares=r.html.xpath(reglascategoria["xpathtitular"]+"/text()")
        listafechas=r.html.xpath(reglascategoria["xpathfecha"]+"/text()")
        listaimg=r.html.xpath(reglascategoria["xpathimg"]+"/@src")
        listaredactores=r.html.xpath(reglascategoria["xpathredactor"]+"/text()")
        listadescripciones=r.html.xpath(reglascategoria["xpathdescripcion"]+"/text()")
    except:
        print("error al cargar datos externos")
    print("url:",urlcategoria)
    reglainterna=reglascategoria["reglainterna"]
    contador=0
    contrep=0 #contador de las urls que ya se encuentran en la base de datos si son mas de dos pasamos a la siguiente categoria
    for urlnot in listaurls:
        if not("http" in urlnot and urlnot!=""):
                urlnot=urlprincipal+urlnot
        cantidadnot=len(list(db["noticia"].find({"urlnoticia":urlnot})))
        if cantidadnot==0:
            
            titular=""
            resumen=""
            fecha=""
            urlimagen=""
            redactor=""
            resumen=""
            parrafos=""
            desimg=""
            hashtags=""
            try:
                titular=listastitulares[contador]
            except:
                print("error titular categoria")
            try:
                fecha=listafechas[contador]
            except:
                print("error fecha categoria")
            try:
                urlimagen=listaimg[contador]
            except:
                print("error imagen categoria")
                urlimagen=""
            try:
                redactor=listaredactores[contador]
            except:
                print("error redactor categoria")
            try:
                resumen=listadescripciones[contador]
            except:
                print("error redactor categoria")
            if reglainterna!="" and reglainterna!="ninguno":
                r2 = await asession.get(urlnot)
                try:
                    titular=r2.html.xpath(reglainterna["xptitular"]+"/text()")[0]
                except:
                    print("no se pudo cargar el titular")
                try:
                    resumen=r2.html.xpath(reglainterna["xpresumen"]+"/text()")[0]
                except:
                    print("no se pudo cargar el titular")
                try:
                    urlimagen=r2.html.xpath(reglainterna["xpimg"]+"/@data-srcset")[0]
                except(Exception):
                    print("error al cargar imagen srcset")
                    print(Exception)
                try:
                    if urlimagen=="" or urlimagen==None: 
                        urlimagen=r2.html.xpath(reglainterna["xpimg"]+"/@src")[0]
                        if not urlprincipal in urlimagen:
                                urlimagen=urlprincipal+urlimagen
                except(Exception):
                    print("error al cargar imagen src")
                    print(Exception)
                try:
                    if urlimagen=="" or urlimagen==None: 
                        urlimagen=r2.html.xpath(reglainterna["xpimg"]+"/@href")[0]
                except:
                    print("no se pudo cargar imagen href")
                    print(Exception)
                try:
                    desimg=r2.html.xpath(reglainterna["xpdesimg"]+"/text()")[0]
                except:
                    print("no se pudo cargar el titular")
                try:
                    redactor=r2.html.xpath(reglainterna["xpredactor"]+"/text()")[0]
                except:
                    print("no se pudo cargar el titular")
                try:
                    listafecha=r2.html.xpath(reglainterna["xpfecha"]+"/text()")
                    for fe in listafecha:
                        fecha=fecha+fe
                except:
                    print("no se pudo cargar el titular")
                try:
                    listaparrafos=r2.html.xpath(reglainterna["xpparrafos"]+"/text()")
                    for p in listaparrafos:
                        parrafos=parrafos+p
                except:
                    print("no se pudo cargar el titular")
                try:
                    hashtags=r2.html.xpath(reglainterna["xphashtags"]+"/text()")
                except:
                    print("no se pudo cargar el titular")
                r2.close()
            
            noticia={
                "urlfuente":urlprincipal,
                "urlnoticia":urlnot,
                "categoria":categoria,
                "estitular":False,
                "titular":titular,
                "resumen":resumen,
                "redactor":redactor,
                "urlimagen":urlimagen,
                "desimagen":desimg,
                "fecha":fecha,
                "fechaasig":datetime.today(),
                "parrafos":parrafos,
                "hashtags":hashtags
                }
            #print(noticia)
            añadirnoticia(noticia)
            
        else:
            contrep+=1
        if contrep>=2:
            break #en caso de encontrar mas de dos notiicias repetidas saltamos de categoria
        contador=contador+1
    r.close()
    try:
        await asession.close()
    except:
        print("No se pudo cerrar sesion")

def añadirnoticia(noticia):
    cantidadnot=len(list(db["noticia"].find({"urlnoticia":noticia["urlnoticia"]})))
    print(noticia["urlnoticia"])
    print(noticia["titular"])
    print(noticia["fecha"])
    if noticia["urlnoticia"]!="" and noticia["titular"]!="" and noticia["titular"]!="\n" and cantidadnot==0:
        db["noticia"].insert_one(noticia)
        generarnotificacion(noticia)
        print("Noticia añadida")
    else:
        print("No se añadio la pagina web...")
        if cantidadnot!=0:
            print("Se encontro la url en la base de datos")
def monitorearpagina(urlpagina):
    colpagina=db["paginanoticia"].find_one({"url":ObjectId(str(urlpagina))})
    #print(colpagina)
    listareglasportada=colpagina["portada"]
    listareglascategoria=colpagina["categorias"]
    #print("listacat",listareglascategoria)
    for portada in listareglasportada:
        urlportada=portada["urlportada"]
        idreglap=portada["idregla"]
        Noticia=consultarportada(urlpagina,urlportada,idreglap).result()
        
        #cargamos la regla de la portada
        #loop = asyncio.new_event_loop()
        #Noticia=loop.run_until_complete(consultarportada(urlpagina,urlportada,idreglap))
        #print(Noticia)
        #cargamos la pagina web de la portada a la base de datos
    for categoria in listareglascategoria:
        print("categoria",categoria)
        #loop = asyncio.new_event_loop()
        monitorearcat(urlpagina,categoria["url"],categoria["idcategoria"],categoria["idregla"]).result()
        #loop.run_until_complete(monitorearcat(urlpagina,categoria["url"],categoria["idcategoria"],categoria["idregla"]))
        print("////////////////////////////")

        

def monitoriartodaslaspaginas():
    listapaginanoticias=db["paginanoticia"].find()
    for paginanoticias in listapaginanoticias:
        urlprincipal=paginanoticias["url"]
        listaportada=paginanoticias["portada"]
        listareglascategoria=paginanoticias["categorias"]
        for portada in listaportada:
            urlportada=portada["urlportada"]
            idreglap=portada["idregla"]
            #cargamos la regla de la portada
            #loop = asyncio.new_event_loop()
            #Noticia=loop.run_until_complete(consultarportada(urlprincipal,urlportada,idreglap))
            #print(Noticia)
            Noticia=consultarportada(urlprincipal,urlportada,idreglap).result()
            
            print("-------------------")
        for categoria in listareglascategoria:
            #print("urlcategoria",categoria["url"])
            #loop = asyncio.new_event_loop()
            #loop.run_until_complete(monitorearcat(urlprincipal,categoria["url"],categoria["idcategoria"],categoria["idregla"]))
            monitorearcat(urlprincipal,categoria["url"],categoria["idcategoria"],categoria["idregla"]).result()
#monitorearpagina("https://www.eldiario.net")
monitoriartodaslaspaginas()
