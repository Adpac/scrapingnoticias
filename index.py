
from audioop import add
from multiprocessing.connection import wait
from os import read
from urllib import response
from flask import Flask, url_for
from re import sub
import re
from flask import Flask, redirect, render_template, session
from flask import make_response
from flask import request
from bson.json_util import dumps
from flask import Flask, session
#from Noticias import paginanoticia
import json
#import Noticias
import threading
from flask_pymongo import PyMongo
import lxml.html as html
from datetime import datetime, timedelta
from passlib.hash import sha512_crypt as sha512
from flask_socketio import SocketIO, send
import time
import asyncio
import pandas as pd
from requestshtml import AsyncHTMLSession
from requestshtml import HTMLSession
from unsync import unsync
from bson.objectid import ObjectId
app = Flask(__name__)
#Conexion a la base de datos
app.config['CORS_HEADERS'] = 'application/json'
app.config["MONGO_URI"] = "mongodb+srv://user:password@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority"
app.secret_key = 'esto-es-una-clave-muy-secreta'
mongodb_client = PyMongo(app)
db = mongodb_client.db
#Inicializando SocketIO
socketio=SocketIO(app)
#Cargando stop words
swsp = pd.read_fwf('Stop Words Spanish.txt', header=None)
stopwordsspanish=swsp[0].to_numpy()
listasw=list(stopwordsspanish)
 
#Elimina stop words dentro de un texto
def eliminarstopwords(texto):
    return ' '.join([word for word in texto.split(' ') if word not in listasw])

#Bot de monitoreo
def scrapingnoticias():
	import Monitoreonoticias
	while(True):
		time.sleep(60)
		try:
			Monitoreonoticias.monitoriartodaslaspaginas()
		except:
			print("ocurrio un error")
tarea=threading.Thread(target=scrapingnoticias).start()

#Encuentra los parametros Xpath de una URL tipo categoria
def obtenerreglaurlcat(url):
	regla=""
	urlarr=url.split("/")
	urlprin=urlarr[0]+"//"+urlarr[2]
	print("//////////")
	print("urlprin", urlprin)
	pagina=db.paginanoticia.find_one({"url":urlprin})
	print("pagina: ",pagina)
	if pagina != None:
		arrayurls=pagina["categorias"]
		for urlsec in arrayurls:
			if urlsec["url"]==url:
				regla=urlsec["idregla"]
				break
	return regla
#Verifica si un Xpath posee un atributo como ser text(), @src, entre otros
def atributoenxpath(xpath):
	retornar=""
	posfin=str(xpath).rfind("/")
	ultimoel=xpath[posfin:]
	if("@" in ultimoel or "text()" in ultimoel):
		retornar=ultimoel
	return retornar
#Obtiene los parametros XPath de una URL tipo portada
def obtenerreglaurlport(url):
	regla=""
	urlarr=url.split("/")
	urlprin=urlarr[0]+"//"+urlarr[2]
	print("//////////")
	print("urlprin", urlprin)
	pagina=db.paginanoticia.find_one({"url":urlprin})
	if pagina != None:
		arrayurls=pagina["portada"]
		for urlsec in arrayurls:
			if urlsec["urlportada"]==url:
				regla=urlsec["idregla"]
				break
	return regla

#edita los datos de una regla
def editarreglaexterna(idregla, xpathurl, xpathtitular, xpathfecha, xpathimg, xpathredactor, xpathdescripcion):
	db.Reglas.update_one({'_id': ObjectId(str(idregla))},{"$set":{
			"xpathurl":xpathurl,
			"xpathtitular":xpathtitular,
			"xpathfecha":xpathfecha,
			"xpathimg":xpathimg,
			"xpathredactor":xpathredactor,
			"xpathdescripcion":xpathdescripcion
			}})

#Carga un sitio web incluyendo los scripts
@unsync
async def cargarpagina(urlpagina):
	asession = AsyncHTMLSession() 
	r = await asession.get(urlpagina,  verify=False)
	contenidopag=r.html.html
	arrayurlpag=urlpagina.split("/")
	protocolo=arrayurlpag[0]
	dominioprin=arrayurlpag[2]
	listaimagenes=r.html.xpath("//@src | //@href")
	print("procesando... imagenes")
	r.close()
	for link in listaimagenes:
		if not ("http" in str(link)):
			if not(dominioprin in link):
				contenidopag=contenidopag.replace('"'+link+'"','"'+ str(protocolo+"//"+dominioprin+link)+'"')
			else:
				contenidopag=contenidopag.replace('"'+link+'"','"'+ str(protocolo+link)+'"')
	#contenidopag=re.sub('<script(.|\n)*?script>', '', contenidopag)
	#contenidopag=re.sub('<body(.|\n)*?>', '<body onbeforeunload="return myFunction()">', contenidopag)
	print("se cargo la pagina web")
	try:
		await asession.close()
		print("sesion cerrada")
	except:
		print("no se pudo cerrar session")
	print("retornando")
	return contenidopag
#carga un sitio web de manera rapida
@unsync
async def cargarpaginarapida(urlpagina):
    asession = AsyncHTMLSession()
    r = await asession.get(urlpagina)
    contenidopag=r.html.html
    arrayurlpag=urlpagina.split("/")
    protocolo=arrayurlpag[0]
    dominioprin=arrayurlpag[2]
    listaimagenes=r.html.xpath("//@src | //@href")
    for link in listaimagenes:
        if not ("http" in str(link)):
            if not(dominioprin in link):
                contenidopag=contenidopag.replace('"'+link+'"','"'+ str(protocolo+"//"+dominioprin+link)+'"')
            else:
                contenidopag=contenidopag.replace('"'+link+'"','"'+ str(protocolo+link)+'"')
	#print("-----------")
	#print(contenidopag)
    return contenidopag
#Carga una pagina y devuelve un valor en base a un Xpath de entrada
@unsync
async def consultarxpath(urlpagina,xpath):
	asession = AsyncHTMLSession() 
	r = await asession.get(urlpagina)
	respuesta=r.html.xpath(xpath)
	#print(respuesta)
	await asession.close()
	return respuesta
#dada una lista de Urls, elimina enlaces no validos
def limpiarenlaces(listaenlace, urlprincipal):
	arrayurlpag=urlprincipal.split("/")
	urlp=arrayurlpag[0]+"//"+arrayurlpag[2]
	print("urlp: ",urlp)
	listaaux=[]
	for enlace in listaenlace:
		if enlace!="" and enlace!="/" and enlace !="#" and enlace!=urlp and enlace != str(urlp+"/"):
			print(enlace)
			if not "http" in enlace:
				listaaux.append(urlp+enlace)
			else:
				listaaux.append(enlace)
	return listaaux

#Ruta Home
@app.route('/')
def home():
	print(__name__)
	#print("redireccionado")
	rol="ninguno"
	if session.get("user")!=None:
		rol=session.get("type")
		
		#print(rol)
	noticias=db.noticia
	listapaginanoticias=list(db.paginanoticia.find({},{"url":1,"_id":0}))
	Noti =list(noticias.find().sort('fechaasig',-1).limit(20))
	hoy=datetime.today()
	ayer=hoy-timedelta(days=1)
	portada=list(noticias.find({'estitular':True, 'fecharecup':{'$lt': hoy, '$gte': ayer}}).sort('fechaasig',-1).limit(20))
	listacategorias=list(db.Categoria.find({}))
	Noticiascat=list(noticias.find({"categoria":"6283257b2964b7cbd0b5a9ab"}).sort('fechaasig',-1).limit(20))
	noticiaspagina=[]
	if len(listapaginanoticias)>0:
		urlfuente=listapaginanoticias[0]["url"]
		if urlfuente[-1:]=="/":
			urlfuente=urlfuente[0:-1]
		noticiaspagina=list(noticias.find({"urlfuente": urlfuente}).sort('fechaasig',-1).limit(20))
	#print(noticiaspagina)

	return render_template('home.html',Noticia=Noti, portada=portada,listacategorias=listacategorias, Noticiascat=Noticiascat, listapaginanoticias=listapaginanoticias, noticiaspagina=noticiaspagina)

#Ruta cerrar sesion
@app.route('/cerrarsesion')
def cerrarsesion():
	session.clear()
	return redirect(url_for('home'))

#Enviar notificaciones al usuario mediante SocketIO
@socketio.on('message')
def enviarnotificacion(msg):
	print("mensaje: "+ msg)
	send(msg,broadcast=True)

#El usuario recibe las ultimas notificaciones
@app.route("/ajaxsolicitarnoti", methods=['POST'])
def ajaxsolicitarnoti():
	user=request.form['user']
	print(user)
	colnot=db.noticia
	Noti =list(colnot.find({},{"titular":1,"parrafos":1,"urlfuente":1, "urlnoticia":1, "urlimagen":1}).sort("fechaasig",-1).limit(20))
	respuesta=dumps(Noti)
	return respuesta
	
#ruta Abotut
@app.route('/about')
def about():
	return render_template('about.html')
#ruta gestionar paginas
@app.route('/gestionarpaginas')
def gestionarpaginas():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador") :
		listapaginanoticias=list(db.paginanoticia.find({},{"url":1,"_id":0}))
		return render_template('gestionarpaginas.html', listapaginanoticias=listapaginanoticias)
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )
#ruta gestionar categorias
@app.route('/gestionarcategorias')
def gestionarcategorias():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador") :
		listacat=list(db.Categoria.find({},))
		return render_template('gestionarcategorias.html', listacat=listacat)
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )
#ruta editar pagina
@app.route('/editarpagina',methods=['GET'])
def editarpagina():
	url = request.args.get('url')
	paginanoticia=db.paginanoticia.find_one({"url":url})
	print(paginanoticia)
	listacategorias=list(db.Categoria.find({}))
	return render_template('editarpagina.html', paginanoticia=paginanoticia, listacategorias=listacategorias)
#ruta buscar noticia
@app.route('/buscarnoticia', methods=['POST'])
def buscarnoticia():
	if request.method=="POST":
		consulta=request.form['buscar']
		dbnoticias=db.noticia

		Noti =list(dbnoticias.find({"$text": {"$search": consulta}}, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})] ).limit(20))
	
	return render_template('busqueda.html', consulta=consulta, Noticia=Noti)
#ruta inicio de sesion
@app.route('/iniciarsesion')
def iniciarsesion():
	if 'mensaje' in request.args:
		mensaje=request.args["mensaje"]
		#print("Mensaje:", mensaje)
		return render_template('iniciosesion.html', mensaje=mensaje)
	else:
		return render_template('iniciosesion.html')
#ruta validar inicio de sesion, verifica si la sesion es correcta y el tipo de usuario
@app.route('/validariniciarsesion', methods=['POST'])	
def validariniciarsesion():
	if request.method=="POST":
		usuario=request.form['username']
		contraseña=request.form['password']
		colusuario=db["usuario"]
		if colusuario.count_documents({"$and":[{"usuario":usuario }]})==1:
			usuario=colusuario.find_one({"usuario": usuario})
			passcod=usuario['contraseña']
			#print(contraseña)
			#print("passcod", passcod)
			if sha512.verify(str(contraseña), str(passcod)):
				#Datos validos
				print("URL inicial: ",url_for('home'))
				session['user']=str(usuario['usuario'])
				session['type']=str(usuario['rol'])
				print("redireccionando...")
				return redirect(url_for('home'))
			else:

				return redirect(url_for('iniciarsesion',mensaje= "Nombre de usuario no valido y/o contraseña no valida"))
		else:

			return redirect(url_for('iniciarsesion', mensaje= "Nombre de usuario no valido y/o contraseña no valida"))

#ruta editar datos de usuario
@app.route('/editarusuario')
def editarusuario():
	if session.get("user")!=None:
		rol=session.get("type")
		print(rol)
		return render_template('Editarusuario.html')
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta registrar usuario	
@app.route('/registrarusuario', methods=['POST'])
def registrarusuario ():
	#Se registra al usuario en la base de datos
	mensaje=""
	if request.method=="POST":
		ci=request.form["ci"]
		usuario=request.form["usuario"]
		nombres=request.form["nombres"]
		apellidos=request.form["apellidos"]
		rol=request.form["tipousuario"]
		colusuario=db["usuario"]
		#verificamos si el numero de carnet esta agregado
		if colusuario.count_documents({"ci":ci })<1:
			#verificamos si el nombre de usuario se encuentra agregado
			if colusuario.count_documents({"usuario":usuario })<1:
				#insertamos los datos del usuario en la base de datos
				contraseña=sha512.hash(ci)
				print(contraseña)
				sol={"ci":ci, "usuario":usuario, "nombres":nombres, "apellidos":apellidos, "rol": rol, "contraseña":contraseña}
				colusuario.insert_one(sol)
				mensaje="Se registro al Usuario con exito"
				mensajesec="La contraseña del usuario sera su numero de carnet sin extencion"
				return render_template("mensaje.html", title="Necesita confirmar correo", mensaje=mensaje, mensajesec=mensajesec)
			else:
				return redirect(url_for('registro', mensaje="El nombre de usuario ya se encuentra en la base de datos"))
		else:	
			return redirect(url_for('registro',mensaje= "El numero de carnet ya se encuentra en la base de datos"))


#ruta reglas categoria, Aqui se seleccionan los parametros Xpath para una nueva URL tipo categoria
@app.route('/reglascategoria', methods=['GET','POST'])
def reglascategoria():
	#https://www.la-razon.com/nacional/
	#https://erbol.com.bo/nacional
	#https://www.eldiario.net/portal/category/nacional/
	#https://www.paginasiete.bo/nacional/
	url="https://www.paginasiete.bo/nacional/"
	editar=False
	if(request.method=="POST"):
		url=request.form["urlcategoria"]
		categoria=request.form["categoria"]
		texto=cargarpagina(url).result()
		#texto=asyncio.run(cargarpagina(url))
		#loop = asyncio.new_event_loop()
		#asyncio.set_event_loop(loop)
		#texto=loop.run_until_complete(cargarpagina(url))
		#loop.close()

	arrayurlext=url.split("/")
	urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
	listareglas=list(db["Reglas"].find({"urlprincipal":urlprincipal, "tiporegla":"categoria"}))
	#print("Lista reglas: ",listareglas)
	css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpath.css">'

	iniciobody=re.search("<body.*>",texto)
	iniciohead=re.search("<head.*>",texto)
	#print(iniciobody.end)

	#Entre la parte 1 y la 2 concatenamos css y scripts
	#entre la parte2 y la 3 concatenamos la cabecera
	dochtml=css+texto
	reglaext=obtenerreglaurlcat(url)
	print("regla externa:,,",reglaext)
	if reglaext!="":
		print("llegue aqui.....")
		response=make_response(render_template('xpathselector.html', debug=True, url=url, texto=dochtml, categoria=categoria, listareglas=listareglas, editar=True, idregla=reglaext))
		return response
	else:
		response=make_response(render_template('xpathselector.html', debug=True, url=url, texto=dochtml, categoria=categoria, listareglas=listareglas, editar=editar))
		return response

#ruta editar reglas categoria, Aqui se editan los parametros Xpath para una URL tipo categoria	existente
@app.route('/editreglascategoria', methods=['GET'])
def editreglascategoria():
	#https://www.la-razon.com/nacional/
	#https://erbol.com.bo/nacional
	#https://www.eldiario.net/portal/category/nacional/
	#https://www.paginasiete.bo/nacional/
	url="https://www.paginasiete.bo/nacional/"
	editar=True
	if(request.method=="GET"):
		url=request.args.get("urlcategoria")
		categoria=request.args.get("categoria")
		idregla=request.args.get("idr")
		print("idregla",idregla)
		texto=cargarpagina(url).result()
		#texto=asyncio.run(cargarpagina(url))
		#loop = asyncio.new_event_loop()
		#asyncio.set_event_loop(loop)
		#texto=loop.run_until_complete(cargarpagina(url))
		#loop.close()
	arrayurlext=url.split("/")
	urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
	listareglas=list(db["Reglas"].find({"urlprincipal":urlprincipal, "tiporegla":"categoria"}))
	#print("Lista reglas: ",listareglas)
	css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpath.css">'

	iniciobody=re.search("<body.*>",texto)
	iniciohead=re.search("<head.*>",texto)
	#print(iniciobody.end)

	#Entre la parte 1 y la 2 concatenamos css y scripts
	#entre la parte2 y la 3 concatenamos la cabecera
	dochtml=css+texto
	
	response=make_response(render_template('xpathselector.html', debug=True, url=url, texto=dochtml, categoria=categoria, listareglas=listareglas, editar=editar, idregla=idregla))
	return response
#ruta editreglas portada aqui se editan los parametros de una nueva URL tipo portada
@app.route('/editreglasportada', methods=['GET'])
def editreglasportada():
	url="https://www.paginasiete.bo/nacional/"
	editar=True
	if(request.method=="GET"):
		url=request.args.get("urlportada")
		idregla=request.args.get("idr")
		print("idregla",idregla)
		texto=cargarpagina(url).result()
		#texto=asyncio.run(cargarpagina(url))
		#loop = asyncio.new_event_loop()
		#asyncio.set_event_loop(loop)
		#texto=loop.run_until_complete(cargarpagina(url))
		#loop.close()
	arrayurlext=url.split("/")
	urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
	listareglas=list(db["Reglas"].find({"urlprincipal":urlprincipal, "tiporegla":"portada"}))
	#print("Lista reglas: ",listareglas)
	css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpathnoticias.css">'

	iniciobody=re.search("<body.*>",texto)
	iniciohead=re.search("<head.*>",texto)
	#print(iniciobody.end)
	parte1=texto[0:iniciohead.end()]

	parte2=texto[iniciohead.end():iniciobody.end()]

	parte3=texto[iniciobody.end():]
	#Entre la parte 1 y la 2 concatenamos css y scripts
	#entre la parte2 y la 3 concatenamos la cabecera
	dochtml=css+parte1+css+parte2+parte3

	response=make_response(render_template('addportada.html',title="evaluarpag", debug=True, url=url, texto=dochtml, listareglas=listareglas, editar=editar, idregla=idregla))
	return response
#Ruta reglas noticia, aqui se seleccionan los parametros Xpath dentro de una noticia
@app.route('/reglasnoticia')
def reglasnoticia():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador"):
		print("llegue a reglas noticia")
		tipo=request.args["tipo"]
		jsondatos=request.args["datosregla"]
		idreglaexterna=request.args["idreglaexterna"]
		cambios=request.args["cambios"]
		reglaex=[]
		reglainterna=[]
		if(idreglaexterna!="ninguno"):
			print(idreglaexterna)
			reglaex=db.Reglas.find_one({"_id":ObjectId(str(idreglaexterna))})
			reglainterna=reglaex["reglainterna"]
			
		categoria=""
		urlext=request.args["urlext"]
		url=request.args["urlnoticia"]
		texto=cargarpagina(url).result()
		#texto=asyncio.run(cargarpagina(url))
		#loop = asyncio.new_event_loop()
		#asyncio.set_event_loop(loop)
		#texto=loop.run_until_complete(cargarpagina(url))
		#loop.close()
		css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpathnoticias.css">'
		iniciobody=re.search("<body.*>",texto)
		iniciohead=re.search("<head.*>",texto)
		#print(iniciobody.end)
		arrayurlext=urlext.split("/")
		urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]

		listareglas=list(db["Reglas"].find({"urlprincipal":urlprincipal, "tiporegla":"noticias"}))

		#Entre la parte 1 y la 2 concatenamos css y scripts
		#entre la parte2 y la 3 concatenamos la cabecera
		dochtml=css+texto
		if(tipo=="categoria"):
			categoria=request.args["categoria"]
		
		response=make_response(render_template('xpathselectornoticias.html', debug=True, url=url, texto=dochtml, tipo=tipo, jsonp1=jsondatos, urlext=urlext, listareglas=listareglas, categoria=categoria, editar=idreglaexterna, reglainterna=reglainterna, cambios=cambios))
		return response
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#Agrega
@app.route('/agregar')
#Redireccion para agregar nuevas URLs de noticia
def agregar():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador"):
		listacategorias=list(db.Categoria.find())
		return render_template('agregar.html',title="agregar", listacategorias=listacategorias)
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta editreglas portada aqui se crean los parametros de una nueva URL tipo portada
@app.route('/añadirportada', methods=['GET', 'POST'])
#al momento de agregar la nueva pagina llenaremos un formulario para identificar los patrones de la misma
def añadirportada():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador"):
		direccion="addportada.html"
		documento=""
		
		if request.method=='POST':
			url=request.form['urlpaginanoticia']
			print(url)
			texto=cargarpagina(url).result()
			#texto=asyncio.run(cargarpagina(url))
			#loop = asyncio.new_event_loop()
			#syncio.set_event_loop(loop)
			#texto= loop.run_until_complete(cargarpagina(url))
			#loop.close()
			print("dochtml......")
			#print(texto)
			print(".........................")
			css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpathnoticias.css">'
			iniciobody=re.search("<body.*>",texto)
			iniciohead=re.search("<head.*>",texto)

			parte1=texto[0:iniciohead.end()]
			parte2=texto[iniciohead.end():iniciobody.end()]
			parte3=texto[iniciobody.end():]
			documento=css+parte1+parte2+parte3
		reglaportada=obtenerreglaurlport(url)
		if reglaportada!="":
			urlarr=url.split("/")
			urlprin=urlarr[0]+"//"+urlarr[2]
			listareglas=list(db["Reglas"].find({"urlprincipal":urlprin, "tiporegla":"portada"}))
			response=make_response(render_template('addportada.html',title="evaluarpag", debug=True, url=url, texto=documento, listareglas=listareglas, editar=True, idregla=reglaportada))
			return response
		else:
			return render_template(direccion, title="evaluarpag", url=url, texto=documento)
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta validar portada, aqui se validan los parametros XPath de una URL tipo portada
@app.route('/validarportada', methods=['GET', 'POST'])
def validarportada():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador"):
		idreglaexterna="ninguno"
		if request.method=='POST':
			seregistrocambios=request.form["cambiosre"]
			print("src",seregistrocambios)
			idreglaexterna=request.form["reglaseleccionada"]
			editarregla=request.form["editarregla"]
			xpathurl=request.form["inputurl"]
			xpathtitular=request.form["inputtitular"]
			xpathfecha=request.form["inputfecha"]
			xpathimg=request.form["inputimg"]
			xpathredactor=request.form["inputredactor"]
			xpathdescripcion=request.form["inputdescripcion"]
			urlportada=request.form["urlprincipal"]
			arrayurlext=urlportada.split("/")
			urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
			jsondatos={
				"urlprincipal":urlprincipal,
				"urlportada":urlportada,
				"tiporegla":"portada",
				"xpathurl":xpathurl,
				"xpathtitular":xpathtitular,
				"xpathfecha":xpathfecha,
				"xpathimg":xpathimg,
				"xpathredactor":xpathredactor,
				"xpathdescripcion":xpathdescripcion,
				"reglainterna":""
			}
		if request.form.get("continuarform"):
			print("obteniendo enlace")
			tag=atributoenxpath(xpathurl)
			if tag=="":
				lurlnot=consultarxpath(urlportada,str(xpathurl)+"//@href").result()
			else:
				lurlnot=consultarxpath(urlportada,str(xpathurl)).result()
			#lurlnot=asyncio.run(consultarxpath(urlprin,str(xpathurl)+"//@href"))
			#loop = asyncio.new_event_loop()
			#asyncio.set_event_loop(loop)
			#lurlnot= loop.run_until_complete(consultarxpath(urlprin,str(xpathurl)+"//@href"))
			#loop.close()
			print("xpath url", xpathurl)
			print("Url noticia",lurlnot)
			urlnoticia=lurlnot[0]
			if not("http" in urlnoticia):
				urlnoticia=urlprincipal+urlnoticia
			print("redireccionando a reglas noticia")
			print(urlnoticia)
			return redirect(url_for('reglasnoticia', tipo="portada",datosregla=json.dumps(jsondatos), urlnoticia=urlnoticia, urlext=urlportada, idreglaexterna=idreglaexterna,cambios=seregistrocambios ))
		else:
			mensaje=""
			mensajesec=""
			#CONFIGURACION DE LAS REGLAS O PARAMETROS..........
			print("idreglaexterna", idreglaexterna)
			if(editarregla!=""):
				if(idreglaexterna!="ninguno"):
					print(editarregla)
					#En este caso modificamos una regla ya existente, editarregla tiene por valor la id de la regla
					editarreglaexterna(editarregla,xpathurl,xpathtitular,xpathfecha,xpathimg,xpathredactor,xpathdescripcion)
					mensajesec="Se modificaron los parametros de la regla con exito"
				else:
					#En este caso se creara una nueva regla en base a la regla externa
					reglacat=db.Reglas.find_one({"_id":ObjectId(str(editarregla))},{"_id": 0})
					reglacat["xpathurl"]=xpathurl
					reglacat["xpathtitular"]=xpathtitular			
					reglacat["xpathfecha"]=xpathfecha
					reglacat["xpathimg"]=xpathimg
					reglacat["xpathredactor"]=xpathredactor
					reglacat["xpathdescripcion"]=xpathdescripcion
					addreglaext=db['Reglas'].insert_one(reglacat)
					idreglaexterna=addreglaext.inserted_id
					print("llegue a este caso")
					mensajesec="Se crearon nuevos parametros para esta URL: "+urlportada
			else:
				if idreglaexterna=="ninguno":
					#si la id regla externa==ninguno entonces se creara una nueva regla
					addreglaext=db['Reglas'].insert_one(jsondatos)
					idreglaexterna=addreglaext.inserted_id
					mensajesec="Se crearon nuevos parametros para la URL: "+urlportada
				else:
					#Si la regla existe entonces la id regla sera establecida
					mensajesec="Se asignaron parametros existentes a esta URL: "+urlportada
			#CONFIGURACION DE LA portada

			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos la portada
				#verificamos si la urlportada existe
				arrayportadas=paginanoticia[0]["portada"]
				print("Arrayportadas",arrayportadas)
				portadasaux=[]
				añadircat=True
				for port in arrayportadas:
					if port["urlportada"]==urlportada:
						#en caso de existir la urlcategorica cambiamos la portada a la nueva regla
						añadircat=False
						port["idregla"]=idreglaexterna
						mensaje="Se modificó la URL"
					portadasaux.append(port)
				print("portadasaux",portadasaux)
				print("///////////")
				arrayportadas=portadasaux
				if añadircat:
					#en caso de que no se haya encontrado una url categorica entonces se añadira la misma
					portada={
						"url":urlportada,
						"idportada":request.form["portada"],
						"idregla":idreglaexterna
					}
					arrayportadas.append(portada)
					mensaje="Se añadio una nueva URL "
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "portada": arrayportadas }})
			else:
				#en caso de que la url principal de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[portada],
					"ultimarevision":datetime.now()- datetime.timedelta(days = 1)
				}
				db["paginanoticia"].insert_one(paginanoticia)
				mensaje="URL Añadida con exito"
				mensajesec="El sistema empezara a recolectar noticias de: "+urlprincipal+"\nSe recopilaran datos de la URL"+urlportada
			return render_template("mensaje.html", title="evaluarpag", mensaje=mensaje, mensajesec= mensajesec )
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta validar url categoria, aqui se validan los parametros xpath de una URL tipo categoria
@app.route('/validarurlcategoria', methods=['GET', 'POST'])
def validarurlcategoria():
	if session.get('type') !=None and (session['type']=="admingen" or session['type']=="administrador"):
		idreglaexterna="ninguno"
		if request.method=='POST':
			editarregla=request.form["editarregla"]
			if "reglaseleccionada" in request.form:
				seregistrocambios=request.form["cambiosre"]
				idreglaexterna=request.form["reglaseleccionada"]
			categoria=request.form["categoria"]
			xpathurl=request.form["inputurl"]
			xpathtitular=request.form["inputtitular"]
			xpathfecha=request.form["inputfecha"]
			xpathimg=request.form["inputimg"]
			xpathredactor=request.form["inputredactor"]
			xpathdescripcion=request.form["inputdescripcion"]
			urlcategoria=request.form["urlprincipal"]
			print("urlprin", urlcategoria)
			arrayurlext=urlcategoria.split("/")
			urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
			jsondatos={
				"urlprincipal":urlprincipal,
				"urlcategoria":urlcategoria,
				"tiporegla":"categoria",
				"xpathurl":xpathurl,
				"xpathtitular":xpathtitular,
				"xpathfecha":xpathfecha,
				"xpathimg":xpathimg,
				"xpathredactor":xpathredactor,
				"xpathdescripcion":xpathdescripcion,
				"reglainterna":""
			}
		if request.form.get("continuarform"):
			#print("obteniendo enlace")
			tag= atributoenxpath(xpathurl)
			lurlnot=""
			if tag=="":
				lurlnot=consultarxpath(urlcategoria,str(xpathurl)+"//@href").result()
			else:
				lurlnot=consultarxpath(urlcategoria,str(xpathurl)).result()
			#lurlnot=asyncio.run(consultarxpath(urlprin,str(xpathurl)+"//@href"))
			#loop = asyncio.new_event_loop()
			#asyncio.set_event_loop(loop)
			#lurlnot= loop.run_until_complete(consultarxpath(urlprin,str(xpathurl)+"//@href"))
			#loop.close()
			urlnoticia=lurlnot[0]
			print("redireccionando a reglas noticia")
			
			if not("http" in urlnoticia):
				urlnoticia=urlprincipal+urlnoticia
			#print(urlnoticia)
			#print("urlp: ",urlprincipal)
			return redirect(url_for('reglasnoticia', tipo="categoria",datosregla=json.dumps(jsondatos), urlnoticia=urlnoticia, urlext=urlcategoria, categoria=categoria, idreglaexterna=idreglaexterna, cambios=seregistrocambios))
		else:
			mensaje=""
			mensajesec=""
			#CONFIGURACION DE LAS REGLAS O PARAMETROS..........
			print("idreglaexterna", idreglaexterna)
			if(editarregla!=""):
				if(idreglaexterna!="ninguno"):
					print(editarregla)
					#En este caso modificamos una regla ya existente, editarregla tiene por valor la id de la regla
					editarreglaexterna(editarregla,xpathurl,xpathtitular,xpathfecha,xpathimg,xpathredactor,xpathdescripcion)
					mensajesec="Se modificaron los parametros de la regla con exito"
				else:
					#En este caso se creara una nueva regla en base a la regla externa
					reglacat=db.Reglas.find_one({"_id":ObjectId(str(editarregla))},{"_id": 0})
					reglacat["xpathurl"]=xpathurl
					reglacat["xpathtitular"]=xpathtitular			
					reglacat["xpathfecha"]=xpathfecha
					reglacat["xpathimg"]=xpathimg
					reglacat["xpathredactor"]=xpathredactor
					reglacat["xpathdescripcion"]=xpathdescripcion
					addreglaext=db['Reglas'].insert_one(reglacat)
					idreglaexterna=addreglaext.inserted_id
					mensajesec="Se crearon nuevos parametros para esta URL: "+urlcategoria
			else:
				if idreglaexterna=="ninguno":
					#si la id regla externa==ninguno entonces se creara una nueva regla
					addreglaext=db['Reglas'].insert_one(jsondatos)
					idreglaexterna=addreglaext.inserted_id
					mensajesec="Se crearon nuevos parametros para la URL: "+urlcategoria
				else:
					#Si la regla existe entonces la id regla sera establecida
					mensajesec="Se asignaron parametros existentes a esta URL: "+urlcategoria
			#CONFIGURACION DE LA CATEGORIA

			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos la categoria
				#verificamos si la urlcategoria existe
				arraycategorias=paginanoticia[0]["categorias"]
				print("Arraycategorias",arraycategorias)
				categoriasaux=[]
				añadircat=True
				for cat in arraycategorias:
					if cat["url"]==urlcategoria:
						#en caso de existir la urlcategorica cambiamos la categoria a la nueva regla
						añadircat=False
						cat["idregla"]=idreglaexterna
						mensaje="Se modificó la URL"
					categoriasaux.append(cat)
				print("Categoriasaux",categoriasaux)
				print("///////////")
				arraycategorias=categoriasaux
				if añadircat:
					#en caso de que no se haya encontrado una url categorica entonces se añadira la misma
					categoria={
						"url":urlcategoria,
						"idcategoria":request.form["categoria"],
						"idregla":idreglaexterna
					}
					arraycategorias.append(categoria)
					mensaje="Se añadio una nueva URL "
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "categorias": arraycategorias }})
			else:
				#en caso de que la url principal de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[],
					"categorias":[categoria],
					"ultimarevision":datetime.now()- datetime.timedelta(days = 1)

				}
				db["paginanoticia"].insert_one(paginanoticia)
				mensaje="URL Añadida con exito"
				mensajesec="El sistema empezara a recolectar noticias de: "+urlprincipal+"\nSe recopilaran datos de la URL"+urlcategoria
			return render_template("mensaje.html", title="evaluarpag", mensaje=mensaje, mensajesec= mensajesec )
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#Ruta cambiar contraseña, permite al usuario cambiar su contraseña 
@app.route("/cambiarcontraseña", methods=["POST"])
def cambiarcontraseña():
	if session.get('type') !=None:
		mensaje=""
		mensajesec=""
		contant=request.form["passwordactual"]
		contnueva=request.form["password"]
		nusuario=request.form["nusuario"]
		#buscando al usuario
		usuario=db.usuario.find_one({"usuario":nusuario})
		if sha512.verify(str(contant), str(usuario["contraseña"])):
			contraseñanueva=sha512.hash(contnueva)
			db.usuario.update_one({"usuario":nusuario},{"$set":{"contraseña":contraseñanueva}})
			mensaje="Contraseña cambiada con exito"
		else:
			mensaje="No se cambio la contraseña"
			mensajesec="Las contraseñas no coinciden por favor ingrese su contraseña corecta"
		return render_template("mensaje.html", title="evaluarpag", mensaje=mensaje, mensajesec= mensajesec )
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta editar datos de usuario
@app.route("/editardatosusuario", methods=["POST"])
def editardatosusuario():
	nusuario=request.form["usuarioac"]
	nusuarionuevo=request.form["usuario"]
	ci=request.form["ci"]
	nombres=request.form["nombres"]
	apellidos=request.form["apellidos"]
	rol=request.form["tipousuario"]
	db.usuario.update_one({"usuario":nusuario},{"$set":{"usuario":nusuarionuevo,"ci":ci,"nombres":nombres,"apellidos":apellidos,"rol":rol}})
	return render_template("mensaje.html", title="evaluarpag", mensaje="Operación exitosa", mensajesec= "Se cambiaron los datos del usuario:"+nusuarionuevo )

#Ruta subir pagina, añade una nueva pagina a la base de datos, incluyendo URL, y Reglas o parametros XPath
@app.route("/subirpagina", methods=["POST"])
def subirpagina():
	mensaje=""
	mensajesec=""
	if request.method=='POST':
		idrext=request.form["reglaex"]
		urlpaginaexterna=request.form["urlexterna"]
		reglaex=request.form["datosreglaexterna"]
		#xpath de las noticias
		xptitularnot=request.form['input1']
		xpresumennot=request.form['input2']
		xpimgnot=request.form['input3']
		xpdesimgnot=request.form['input4']
		xpredactornot=request.form['input5']
		xpfechanot=request.form['input6']
		xpparrafos=request.form['input7']
		xphshtag=request.form['input8']
		#Añadimos los datos a la base de datos de MongoDb (coleccion Paginanoticias)
		arrurlexterna=urlpaginaexterna.split("/")
		#print("urlexterna: "+urlpaginaexterna)
		urlprincipal=arrurlexterna[0]+"//"+arrurlexterna[2]

		#Cargando la regla interna
		reglaint={
			"xptitular":xptitularnot,
			"xpresumen":xpresumennot,
			"xpimg":xpimgnot,
			"xpdesimg":xpdesimgnot,
			"xpredactor":xpredactornot,
			"xpfecha":xpfechanot,
			"xpparrafos":xpparrafos,
			"xphashtags":xphshtag
		}



		#print("reglaext",reglaex)
		#print("//*/*/**/*/*/*/*/*")
		#Poniendo la regla interna dentro de la regla externa
		reglaexterna=json.loads(reglaex)
		reglaexterna['reglainterna']=reglaint
		#Añadiendo la regla externa
		if idrext!="ninguno" and idrext!="":
			db.Reglas.update_one({'_id': ObjectId(str(idrext))},{"$set":reglaexterna})
			mensajesec="Se editaron los parametros de recoleccion de la página"
		else:
			addreglaext=db['Reglas'].insert_one(reglaexterna)
			idrext=addreglaext.inserted_id
			mensajesec="se añadieron nuevos parametros para recolectar noticias de la página "+urlpaginaexterna
		if(reglaexterna['tiporegla']=="categoria"):
			#Si la regla es una categoria añadimos la categoria dentro de la URL
			categoria={
				"url":urlpaginaexterna,
				"idcategoria":request.form["categoria"],
				"idregla":idrext
			}
			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos la categoria
				#primero verificamos que la url existe, con el fin de modificar o editar laregla
				arraycategorias=paginanoticia[0]["categorias"]
				añadircat=True
				aux=[]
				for cat in arraycategorias:
					if cat["url"]==urlpaginaexterna:
						cat["idcategoria"]=request.form["categoria"]
						cat["idregla"]=idrext
						añadircat=False
					aux.append(cat)
				arraycategorias=aux
				if añadircat:
					arraycategorias.append(categoria)
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "categorias": arraycategorias }})
			else:
				#en caso de que la url de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[],
					"categorias":[categoria],
					"ultimarevision":datetime.now()- datetime.timedelta(days = 1)
				}
				db["paginanoticia"].insert_one(paginanoticia)
		else:
			#Si la regla externa es de tipo portada
			portada={
				"urlportada":urlpaginaexterna,
				"idregla":idrext
			}
			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos portada
				arrayportadas=paginanoticia[0]["portada"]
				aux=[]
				añadirport=True
				for port in arrayportadas:
					if port["urlportada"]==urlpaginaexterna:
						port["idregla"]=idrext
						añadirport=False
						mensaje="Se modifico la url"
					aux.append(port)
				arrayportadas=aux
				if añadirport:
					arrayportadas.append(portada)
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "portada": arrayportadas }})
			else:
				#en caso de que la url de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[portada],
					"categorias":[],
					"ultimarevision":datetime.now()- datetime.timedelta(days = 1)
				}
				db["paginanoticia"].insert_one(paginanoticia)
				mensaje="Se añadio la URL"


	return render_template("mensaje.html", title="evaluarpag", mensaje=mensaje, mensajesec=mensajesec )
#Ruta gestionar usuarios
@app.route("/gestionarusuarios")
def gestionarusuarios():
	if session.get('type') !=None and session['type']=="admingen":
		listausuarios=list(db.usuario.find({},{"contraseña":0}))
		return render_template("gestionarusuarios.html", title="gestionar usuarios", listausuarios=listausuarios)
	else:
		return render_template("mensaje.html", title="evaluarpag", mensaje="Acceso no autorizado", mensajesec="Usted no tiene autorización para ingresar a esta URL" )

#ruta recibir noticia esto es una prueba...
@app.route("/recibirnot", methods=["POST"])
def recibirnot():
	print("solicitud nueva")
	print(request.form.to_dict())
	mensaje=request.form['mensaje']
	print("nueva Noticia")
	print(mensaje)
	response={'status':200}
	return(response)

#ruta ajax categorias, envia noticias de una categoria en formato Json
@app.route("/ajaxcategorias", methods=["POST"])
def ajaxcategorias():
	categoria=request.form['categoria']
	noticias=db.noticia	
	cat=str(categoria)
	#print("Categoria: ",cat)
	Noticiascat=list(noticias.find({"categoria":cat}).sort("fechaasig",-1).limit(20))
	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)

#ruta ajax fuente, envia noticias segun su fuente en formato json
@app.route("/ajaxfuente", methods=["POST"])
def ajaxfuente():
	
	urlfuente=request.form['urlfuente']
	if urlfuente[-1]=="/":
		urlfuente=urlfuente[:-1]
	noticias=db.noticia	
	noticiaspagina=list(noticias.find({"urlfuente":urlfuente}).sort("fechaasig",-1).limit(20))

	response={
		'status': 200,
		'Noticias':dumps(noticiaspagina),
		'id': 1
	}
	return json.dumps(response)

#Ajax cargar categorias, carga nuevas categorias
@app.route("/ajaxcargarcategorias", methods=["POST"])
def ajaxcargarcategorias():
	categoria=request.form['categoria']
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	noticias=db.noticia	
	cat=str(categoria)
	#print("Categoria: ",cat)
	Noticiascat=list(noticias.find({"categoria":cat}).skip(omitir).sort("fechaasig",-1).limit(20))


	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)

#ruta ajax cargar noticia fuente, carga mas noticias segun una fuente
@app.route("/ajaxcargarnotfuente", methods=["POST"])
def ajaxcargarnotfuente():
	urlfuente=request.form['urlfuente']
	if urlfuente[-1]=="/":
		urlfuente=urlfuente[:-1]
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	
	noticias=db.noticia	
	Noticiascat=list(noticias.find({"urlfuente":urlfuente}).skip(omitir).sort("fechaasig",-1).limit(20))

	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)

#Carga mas noticias del apartado principal
@app.route("/ajaxcargarmasnoticias", methods=["POST"])
def ajaxcargarmasnoticias():
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	noticias=db.noticia	
	Noti =list(noticias.find().sort("fechaasig",-1).skip(omitir).limit(20))
	response={
		'status': 200,
		'Noticias':dumps(Noti),
		'id': 1
	}
	return json.dumps(response)
#carga mas resultados de busqueda
@app.route("/ajaxcargarmasbusquedas", methods=["POST"])
def ajaxcargarmasbusquedas():
	numpagina=request.form["numpagina"]
	consulta=request.form["consulta"]
	omitir=20*int(numpagina)
	noticias=db.noticia	
	Noti =list(noticias.find({"$text": {"$search": consulta}}, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})] ).skip(omitir).limit(20))
	response={
		'status': 200,
		'Noticias':dumps(Noti),
		'id': 1
	}
	return json.dumps(response)
#Añade una nueva categoria
@app.route("/ajaxañadircategoria", methods=["POST"])
def ajaxañadircategoria():
	categoria=request.form["categoria"]
	insertar=db.Categoria.insert_one({"cat":categoria})
	#print("Añadido: ",insertar.inserted_id)
	response={
		'status':200,
		'respuesta':'Categoria agregada exitosamente',
		'id':str(insertar.inserted_id)
	}
	return json.dumps(response)
#Busca las noticias relacionadas con respecto a una noticia
@app.route("/ajaxbuscarnoticiasrelacionadas", methods=["POST"])
def ajaxbuscarnoticiasrelacionadas():
	dbnoticias=db.noticia
	url=request.form["urlnoticia"]
	noticia=dbnoticias.find_one({"urlnoticia":url})
	texto=noticia["titular"]+noticia["parrafos"][0:300]
	texto=str(texto).replace("("," ")
	texto=str(texto).replace(")"," ")
	texto=str(texto).replace(",","")
	texto=str(texto).replace(":","")
	texto=str(texto).replace("\"","")
	texto=texto.lower()
	textosinsw=eliminarstopwords(texto)
	print(textosinsw)
	print("/*/*/*/*/*//")
	Noti =list(dbnoticias.find({"$text": {"$search": textosinsw}, "urlnoticia":{"$ne":url} }, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})]).limit(10))
	response={
		'status': 200,
		'Noticias':dumps(Noti),
		'id': 1
	}
	return json.dumps(response)
#elimina por completo un sitio web añadido a la base de datos
@app.route("/ajaxeliminarpagina", methods=["POST"])
def ajaxeliminarpagina():
	urlpagina=request.form["urlpagina"]
	db.Reglas.delete_many({"urlprincipal":urlpagina})
	db.paginanoticia.delete_one({"url":urlpagina})
	
	response={
		'status': 200,
		'respuesta': "eliminado con exito"
	}
	return json.dumps(response)

#Elimina solo una URL tipo categoria de un sitio web
@app.route("/ajaxeliminarurlcat", methods=["POST"])
def ajaxeliminarurlcat():
	#Este algoritmo elimina una url seleccionada
	#nota ejecutar un algortimo que elimine las reglas en caso de que la regla de la categoria sea la unica
	urlpagina=request.form["urlpagina"]
	urlcategoria=request.form["urlcat"]
	paginanot=db.paginanoticia.find_one({"url":urlpagina})
	listaurlcat=paginanot["categorias"]
	aux=[]
	print(urlcategoria)
	for urlcat in listaurlcat:
		if urlcat["url"]!=urlcategoria:
			aux.append(urlcat)
	
	db["paginanoticia"].update_one({"url":urlpagina},{"$set": { "categorias": aux }})

	response={
		'status': 200,
		'respuesta': "eliminado con exito"
	}
	return json.dumps(response)
#Elimina solo una URL tipo portada de un sitio web
@app.route("/ajaxeliminarurlportada", methods=["POST"])
def ajaxeliminarurlportada():
	#Este algoritmo elimina una url seleccionada
	#nota ejecutar un algortimo que elimine las reglas en caso de que la regla de la categoria sea la unica
	urlpagina=request.form["urlpagina"]
	urlportada=request.form["urlportada"]
	paginanot=db.paginanoticia.find_one({"url":urlpagina})
	listaurlportada=paginanot["portada"]
	aux=[]
	print(urlportada)
	for urlport in listaurlportada:
		if urlport["urlportada"]!=urlportada:
			aux.append(urlport)
	
	db["paginanoticia"].update_one({"url":urlpagina},{"$set": { "portada": aux }})

	response={
		'status': 200,
		'respuesta': "eliminado con exito"
	}
	return json.dumps(response)

#Cambia de la la categoria de una URL tipo categoria
@app.route("/ajaxcambiarcat", methods=["POST"])
def ajaxcambiarcat():

	urlpagina=request.form["urlpagina"]
	urlcategoria=request.form["urlcat"]
	idcatnueva=request.form["categoria"]
	paginanot=db.paginanoticia.find_one({"url":urlpagina})
	listaurlcat=paginanot["categorias"]
	aux=[]
	print(urlcategoria)
	for urlcat in listaurlcat:
		if urlcat["url"]==urlcategoria:
			print("cambiando categoria....")
			urlcat["idcategoria"]=idcatnueva
		aux.append(urlcat)
		
	db["paginanoticia"].update_one({"url":urlpagina},{"$set": { "categorias": aux }})

	response={
		'status': 200,
		'respuesta': "Modificado con exito"
	}
	return json.dumps(response)
#Verifica si un nombre de usuario se encuentra disponible
@app.route("/ajaxvalidarnusuario", methods=["POST"])
def ajaxvalidarnusuario():
	respuesta="false"
	nombreusuario=request.form["nusuario"]
	usuarios=list(db.usuario.find({"usuario":nombreusuario}))
	if(len(usuarios)==0):
		respuesta="true"
	response={
		'status':200,
		'respuesta':respuesta
	}
	return json.dumps(response)
#Elimina a un usuario
@app.route("/ajaxeliminarusuario", methods=["POST"])
def ajaxeliminarusuario():
	iduser=request.form["iduser"]
	db.usuario.delete_one({"_id":ObjectId(iduser)})
	response={
		'status':200,
		'respuesta':"Usuario eliminado"
	}
	return json.dumps(response)
#Edita el nombre de una categoria
@app.route("/ajaxeditarcategoria", methods=["POST"])
def ajaxeditarcategoria():
	idcat=request.form["idcat"]
	nombrecat=request.form["nombrecat"]
	db["Categoria"].update_one({"_id":ObjectId(idcat)},{"$set": { "cat": nombrecat }})
	response={
		'status':200,
		'respuesta':"Categoria cambiada con exito"
	}
	return json.dumps(response)
#verifica se la casilla contraseña y verificar contraseña coinciden
@app.route("/ajaxcoincidencontraseñas", methods=["POST"])
def ajaxcoincidencontraseñas():
	print("llegue aqui-----------")
	respuesta="false"
	contraseña=request.form["contraseña"]
	nusuario=request.form["usuario"]
	print("Usuario: ",nusuario)
	print("**-*-*-*-*-*-")
	usuario=db.usuario.find_one({"usuario":nusuario})
	if sha512.verify(str(contraseña), str(usuario['contraseña'])):
		respuesta="true"
	response={
		'status':200,
		'respuesta':respuesta
	}
	return json.dumps(response)

if __name__ == '__main__':
	app.run(debug=True)
	socketio.run(app,debug=True, port=5004, async_mode='gevent_uwsgi')

	
