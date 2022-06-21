
from audioop import add
from multiprocessing.connection import wait
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
app = Flask(__name__)
conectionurl="mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority"
app.config['CORS_HEADERS'] = 'application/json'
app.config["MONGO_URI"] = "mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority"
app.secret_key = 'esto-es-una-clave-muy-secreta'
mongodb_client = PyMongo(app)
db = mongodb_client.db
salt="nevermore"
socketio=SocketIO(app)
swsp = pd.read_fwf('Stop Words Spanish.txt', header=None)
stopwordsspanish=swsp[0].to_numpy()
listasw=list(stopwordsspanish)
 
def eliminarstopwords(texto):
    return ' '.join([word for word in texto.split(' ') if word not in listasw])

def scrapingnoticias():
	import Monitoreonoticias
	while(True):
		time.sleep(60)
		try:
			Monitoreonoticias.monitoriartodaslaspaginas()
		except:
			print("ocurrio un error")

#tarea=threading.Thread(target=scrapingnoticias).start()
@unsync
async def cargarpagina(urlpagina):
	asession = AsyncHTMLSession() 

	r = await asession.get(urlpagina)

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
	print("se cargo la pagina web")
	try:
		await asession.close()
		print("sesion cerrada")
	except:
		print("no se pudo cerrar session")
	print("retornando")
	return contenidopag

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
@unsync
async def consultarxpath(urlpagina,xpath):
	asession = AsyncHTMLSession() 
	r = await asession.get(urlpagina)
	respuesta=r.html.xpath(xpath)
	#print(respuesta)
	await asession.close()
	return respuesta
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
@app.route('/users',methods=['POST'])
def create_user():
	return{'message':'received'}

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
	Noti =list(noticias.find().sort("fechaasig",-1).limit(20))
	hoy=datetime.today()
	ayer=hoy-timedelta(days=2)
	portada=list(noticias.find({'estitular':True, 'fecharecup':{'$lt': hoy, '$gte': ayer}}).sort("field",-1).limit(20))
	listacategorias=list(db.Categoria.find({}))
	Noticiascat=list(noticias.find({"categoriaprin":"6283257b2964b7cbd0b5a9ab"}).sort("field",-1).limit(20))
	noticiaspagina=[]
	if len(listapaginanoticias)>0:
		urlfuente=listapaginanoticias[0]["url"]
		if urlfuente[-1:]=="/":
			urlfuente=urlfuente[0:-1]
		noticiaspagina=list(noticias.find({"urlfuente": urlfuente}).sort("field",-1).limit(20))
	#print(noticiaspagina)

	return render_template('home.html',Noticia=Noti, portada=portada,listacategorias=listacategorias, Noticiascat=Noticiascat, listapaginanoticias=listapaginanoticias, noticiaspagina=noticiaspagina)

@app.route('/cerrarsesion')
def cerrarsesion():
	session.clear()
	return redirect(url_for('home'))

@socketio.on('message')
def enviarnotificacion(msg):
	print("mensaje: "+ msg)
	send(msg,broadcast=True)

@app.route("/ajaxsolicitarnoti", methods=['POST'])
def ajaxsolicitarnoti():
	user=request.form['user']
	print(user)
	colnot=db.noticia
	Noti =list(colnot.find({},{"titular":1,"parrafos":1,"urlfuente":1, "urlnoticia":1, "urlimagen":1}).sort("fechaasig",-1).limit(20))
	respuesta=dumps(Noti)
	return respuesta
	
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/buscarnoticia', methods=['POST'])
def buscarnoticia():
	if request.method=="POST":
		consulta=request.form['buscar']
		dbnoticias=db.noticia

		Noti =list(dbnoticias.find({"$text": {"$search": consulta}}, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})] ).limit(20))
	
	return render_template('busqueda.html', consulta=consulta, Noticia=Noti)
@app.route('/iniciarsesion')
def iniciarsesion():
	if 'mensaje' in request.args:
		mensaje=request.args["mensaje"]
		#print("Mensaje:", mensaje)
		return render_template('iniciosesion.html', mensaje=mensaje)
	else:
		return render_template('iniciosesion.html')
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
				mensaje="contraseña no valida"
				print(mensaje)
				return redirect(url_for('iniciarsesion',mensaje= "Contraseña no valida"))
		else:
			mensaje="Usuario no valido"
			print(mensaje)
			return redirect(url_for('iniciarsesion', mensaje= "Nombre de usuario no valido"))

	
@app.route('/registro')
def registro():
	#Verificamos si hay un mensaje
	if 'mensaje' in request.args:
		mensaje=request.args["mensaje"]
		print("Mensaje:", mensaje)
		return render_template('registro.html', mensaje=mensaje)
	else:
		return render_template('registro.html')

@app.route('/editarusuario')
def editarusuario():
	if session.get("user")!=None:
		rol=session.get("type")
		print(rol)
	return render_template('Editarusuario.html')
	
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
"""
@app.route('/formpart2', methods=['POST'])
def formpart2():
	xpathtitular=""
	xpathcabecera=""
	urlprincipal=""
	listacategorias=list(db.Categoria.find())
	if request.method=="POST":
		xpathcabecera=request.form["inputcabecera"]
		xpathtitular=request.form["inputtitular"]
		urlprincipal=request.form["urlprincipal"]
	print("urlp",urlprincipal)
	#listaenlaces=scr.obtenerenlaces(urlprincipal,xpathcabecera)
	loop = asyncio.new_event_loop()
	listaenlaces= loop.run_until_complete(consultarxpath(urlprincipal,str(xpathcabecera)+"//@href"))
	listaenlaces=limpiarenlaces(listaenlaces,urlprincipal)
	print("-----------listaenlaces---------")
	print(listaenlaces)

	response=make_response(render_template('formpart2.html', xpathcabecera=xpathcabecera, xpathtitular=xpathtitular, urlprincipal=urlprincipal, lista=listaenlaces, listacategorias=listacategorias))
	print(urlprincipal)
	response.set_cookie('Urlprincipal',urlprincipal)
	response.set_cookie('Xpathtitular',xpathtitular)
	response.set_cookie('Xpathcabecera',xpathcabecera)
	return response

"""



@app.route('/reglascategoria', methods=['POST'])
def reglascategoria():
	#https://www.la-razon.com/nacional/
	#https://erbol.com.bo/nacional
	#https://www.eldiario.net/portal/category/nacional/
	#https://www.paginasiete.bo/nacional/
	url="https://www.paginasiete.bo/nacional/"

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
	parte1=texto[0:iniciohead.end()]

	parte2=texto[iniciohead.end():iniciobody.end()]

	parte3=texto[iniciobody.end():]
	#Entre la parte 1 y la 2 concatenamos css y scripts
	#entre la parte2 y la 3 concatenamos la cabecera
	dochtml=css+parte1+css+parte2+parte3
	
	response=make_response(render_template('xpathselector.html', debug=True, url=url, texto=dochtml, categoria=categoria, listareglas=listareglas))
	return response

@app.route('/reglasnoticia')
def reglasnoticia():
	print("llegue a reglas noticia")
	tipo=request.args["tipo"]
	jsondatos=request.args["datosregla"]
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
	parte1=texto[0:iniciohead.end()]

	parte2=texto[iniciohead.end():iniciobody.end()]

	parte3=texto[iniciobody.end():]
	#Entre la parte 1 y la 2 concatenamos css y scripts
	#entre la parte2 y la 3 concatenamos la cabecera
	dochtml=css+parte1+css+parte2+parte3
	if(tipo=="categoria"):
		categoria=request.args["categoria"]
	
	response=make_response(render_template('xpathselectornoticias.html', debug=True, url=url, texto=dochtml, tipo=tipo, jsonp1=jsondatos, urlext=urlext, listareglas=listareglas, categoria=categoria))
	return response
	


@app.route('/agregar')
#Redireccion para agregar pagina
def agregar():
	listacategorias=list(db.Categoria.find())
	return render_template('agregar.html',title="agregar", listacategorias=listacategorias)

@app.route('/añadirportada', methods=['GET', 'POST'])
#al momento de agregar la nueva pagina llenaremos un formulario para identificar los patrones de la misma
def añadirportada():
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
	return render_template(direccion, title="evaluarpag", url=url, texto=documento)

@app.route('/validarportada', methods=['GET', 'POST'])
def validarportada():
	
	if request.method=='POST':
		xpathurl=request.form["inputurl"]
		xpathtitular=request.form["inputtitular"]
		xpathfecha=request.form["inputfecha"]
		xpathimg=request.form["inputimg"]
		xpathredactor=request.form["inputredactor"]
		xpathdescripcion=request.form["inputdescripcion"]
		urlprin=request.form["urlprincipal"]
		arrayurlext=urlprin.split("/")
		urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
		jsondatos={
			"urlprincipal":urlprincipal,
			"urlportada":urlprin,
			"tiporegla":"portada",
			"xpathurl":xpathurl,
			"xpathtitular":xpathtitular,
			"xpathfecha":xpathfecha,
			"xpathimg":xpathimg,
			"xpathredactor":xpathredactor,
			"xpathdescripcion":xpathdescripcion,
			"idreglainterna":""
		}
	if request.form.get("continuarform"):
		print("obteniendo enlace")
		lurlnot=consultarxpath(urlprin,str(xpathurl)+"//@href").result()
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
		return redirect(url_for('reglasnoticia', tipo="portada",datosregla=json.dumps(jsondatos), urlnoticia=urlnoticia, urlext=urlprin ))
	else:
		addreglaext=db['Reglas'].insert_one(jsondatos)
		portada={
				"urlportada":urlprin,
				"idregla":addreglaext.inserted_id
			}
		paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
		if(len(paginanoticia)>0):
			#en caso de que exista la pagina de noticias añadimos portada
			arrayportadas=paginanoticia[0]["portada"]
			arrayportadas.append(portada)
			db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "portada": arrayportadas }})
		else:
			#en caso de que la url de la pagina no exista
			paginanoticia={
				"url":urlprincipal,
				"portada":[portada],
				"categorias":[]
			}
			db["paginanoticia"].insert_one(paginanoticia)
		return render_template("mensaje.html", title="evaluarpag", mensaje="Se añadio las reglas de la portada a la base de datos", mensajesec="A partir de ahora el sistema empezara a monitorear las noticias de portada de la página: " )
@app.route('/validarurlcategoria', methods=['GET', 'POST'])
def validarurlcategoria():
	idreglaexterna="ninguno"
	if request.method=='POST':
		if "reglaseleccionada" in request.form:
			idreglaexterna=request.form["reglaseleccionada"]
		categoria=request.form["categoria"]
		xpathurl=request.form["inputurl"]
		xpathtitular=request.form["inputtitular"]
		xpathfecha=request.form["inputfecha"]
		xpathimg=request.form["inputimg"]
		xpathredactor=request.form["inputredactor"]
		xpathdescripcion=request.form["inputdescripcion"]
		urlprin=request.form["urlprincipal"]
		print("urlprin", urlprin)
		arrayurlext=urlprin.split("/")
		urlprincipal=arrayurlext[0]+"//"+arrayurlext[2]
		jsondatos={
			"urlprincipal":urlprincipal,
			"urlcategoria":urlprin,
			"tiporegla":"categoria",
			"xpathurl":xpathurl,
			"xpathtitular":xpathtitular,
			"xpathfecha":xpathfecha,
			"xpathimg":xpathimg,
			"xpathredactor":xpathredactor,
			"xpathdescripcion":xpathdescripcion,
			"idreglainterna":""
		}
	if request.form.get("continuarform"):
		#print("obteniendo enlace")
		lurlnot=consultarxpath(urlprin,str(xpathurl)+"//@href").result()
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
		return redirect(url_for('reglasnoticia', tipo="categoria",datosregla=json.dumps(jsondatos), urlnoticia=urlnoticia, urlext=urlprin, categoria=categoria ))
	else:
		print("idreglaexterna", idreglaexterna)
		if idreglaexterna=="ninguno":
			addreglaext=db['Reglas'].insert_one(jsondatos)
			idreglaexterna=addreglaext.inserted_id
		categoria={
			"url":urlprin,
			"idcategoria":request.form["categoria"],
			"idregla":idreglaexterna
		}	
		paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
		if(len(paginanoticia)>0):
			#en caso de que exista la pagina de noticias añadimos la categoria
			arraycategorias=paginanoticia[0]["categorias"]
			arraycategorias.append(categoria)
			db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "categorias": arraycategorias }})
		else:
			#en caso de que la url de la pagina no exista
			paginanoticia={
				"url":urlprincipal,
				"portada":[],
				"categorias":[categoria]
			}
			db["paginanoticia"].insert_one(paginanoticia)
		return render_template("mensaje.html", title="evaluarpag", mensaje="Se añadio las reglas de la portada a la base de datos", mensajesec="A partir de ahora el sistema empezara a monitorear las noticias de portada de la página: " )

@app.route("/subirpagina", methods=["POST"])
def subirpagina():
	idreglainterna="ninguno"
	if request.method=='POST':
		if "reglaseleccionada" in request.form:
			idreglainterna=request.form["reglaseleccionada"]
		tiporeglaexterna=request.form["tiporeglaexterna"]
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
		reglacoin=list(db["Reglas"].find({"tiporegla":"noticias","urlprincipal":urlprincipal,"xptitular":xptitularnot,"xpresumen":xpresumennot,"xpimg":xpimgnot,"xpdesimg":xpdesimgnot,"xpredactor":xpredactornot,"xpfecha":xpfechanot,"xpparrafos":xpparrafos,"xphashtags":xphshtag}))
		if(len(reglacoin)==0):
			#por ninguno añadimos la nueva regla el nuevo id sera 
			colregla={
				"tiporegla":"noticias",
				"urlprincipal":urlprincipal,
				"xptitular":xptitularnot,
				"xpresumen":xpresumennot,
				"xpimg":xpimgnot,
				"xpdesimg":xpdesimgnot,
				"xpredactor":xpredactornot,
				"xpfecha":xpfechanot,
				"xpparrafos":xpparrafos,
				"xphashtags":xphshtag
			}
			addregla=db['Reglas'].insert_one(colregla)
			idreglainterna=addregla.inserted_id
		else:
			idreglainterna=reglacoin[0]["_id"]

		#print("reglaext",reglaex)
		#print("//*/*/**/*/*/*/*/*")
		#añadiendo la regla externa
		reglaexterna=json.loads(reglaex)
		reglaexterna['idreglainterna']=idreglainterna
		addreglaext=db['Reglas'].insert_one(reglaexterna)
		if(reglaexterna['tiporegla']=="categoria"):
			categoria={
				"url":urlpaginaexterna,
				"idcategoria":request.form["categoria"],
				"idregla":addreglaext.inserted_id
			}
			
			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos la categoria
				arraycategorias=paginanoticia[0]["categorias"]
				arraycategorias.append(categoria)
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "categorias": arraycategorias }})
			else:
				#en caso de que la url de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[],
					"categorias":[categoria]
				}
				db["paginanoticia"].insert_one(paginanoticia)
		else:
			#Añadiendo portada
			portada={
				"urlportada":urlpaginaexterna,
				"idregla":addreglaext.inserted_id
			}
			paginanoticia=list(db["paginanoticia"].find({"url":urlprincipal}))
			if(len(paginanoticia)>0):
				#en caso de que exista la pagina de noticias añadimos portada
				arrayportadas=paginanoticia[0]["portada"]
				arrayportadas.append(portada)
				db["paginanoticia"].update_one({"url":urlprincipal},{"$set": { "portada": arrayportadas }})
			else:
				#en caso de que la url de la pagina no exista
				paginanoticia={
					"url":urlprincipal,
					"portada":[portada],
					"categorias":[]
				}
				db["paginanoticia"].insert_one(paginanoticia)

	mensaje="Se añadio la pagina web con exito "
	mensajesec=mensajesec="A partir de ahora se empezara recolectar noticias de esta paginaweb "+urlprincipal
	return render_template("mensaje.html", title="evaluarpag", mensaje=mensaje, mensajesec=mensajesec )

@app.route("/recibirnot", methods=["POST"])
def recibirnot():
	print("solicitud nueva")
	print(request.form.to_dict())
	mensaje=request.form['mensaje']
	print("nueva Noticia")
	print(mensaje)
	response={'status':200}
	return(response)

@app.route("/ajaxcategorias", methods=["POST"])
def ajaxcategorias():
	categoria=request.form['categoria']
	noticias=db.noticia	
	cat=str(categoria)
	#print("Categoria: ",cat)
	Noticiascat=list(noticias.find({"categoriaprin":cat}).sort("fechaasig",-1).limit(20))


	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)
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
@app.route("/ajaxcargarcategorias", methods=["POST"])
def ajaxcargarcategorias():
	categoria=request.form['categoria']
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	noticias=db.noticia	
	cat=str(categoria)
	#print("Categoria: ",cat)
	Noticiascat=list(noticias.find({"categoriaprin":cat}).skip(omitir).sort("fechaasig",-1).limit(20))


	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)

@app.route("/ajaxcargarnotfuente", methods=["POST"])
def ajaxcargarnotfuente():
	urlfuente=request.form['urlfuente']
	if urlfuente[-1]=="/":
		urlfuente=urlfuente[:-1]
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	
	noticias=db.noticia	
	Noticiascat=list(noticias.find({"urlfuente":urlfuente}).sort("fechaasig",-1).skip(omitir).sort("fechaasig",-1).limit(20))

	response={
		'status': 200,
		'Noticias':dumps(Noticiascat),
		'id': 1
	}
	return json.dumps(response)
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
@app.route("/ajaxcargarmastemas", methods=["POST"])
def ajaxcargarmastemas():
	numpagina=request.form["numpagina"]
	omitir=20*int(numpagina)
	coltemas=db.temasdenoticias
	noticias=db.noticia	
	numtemas=list(coltemas.find({}).sort("fechamod",-1).skip(omitir).limit(20))
	listatemas=[]
	for tema in numtemas:
		numtema=tema["numtema"]
		noticiastema=list(noticias.find({"numerotema":numtema}).sort("fechaasig",-1))
		listatemas.append(noticiastema)
	response={
		'status': 200,
		'listatemas':dumps(listatemas),
		'id': 1
	}
	return json.dumps(response)
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
@app.route("/ajaxbuscarnoticiasrelacionadas", methods=["POST"])
def ajaxbuscarnoticiasrelacionadas():
	dbnoticias=db.noticia
	url=request.form["urlnoticia"]
	noticia=dbnoticias.find_one({"urlnoticia":url})
	textosinsw=eliminarstopwords(noticia["titular"])
	#print(textosinsw)
	Noti =list(dbnoticias.find({"$text": {"$search": textosinsw}, "urlnoticia":{"$ne":url} }, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})]).limit(10))
	response={
		'status': 200,
		'Noticias':dumps(Noti),
		'id': 1
	}
	return json.dumps(response)

if __name__ == '__main__':
	app.run(debug=True)
	socketio.run(app,debug=True, port=5004)

	
