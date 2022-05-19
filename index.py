
from multiprocessing.connection import wait
from flask import Flask, url_for
from urllib import response
from flask_cors import CORS, cross_origin
from re import sub
import re
from flask import Flask, redirect, render_template, session
from flask import make_response
from flask import request
from bson.json_util import dumps
from flask import Flask, session
#from Noticias import paginanoticia
import requests
import scraping as scr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
#import Noticias
import threading
from concurrent.futures import ThreadPoolExecutor
from flask_pymongo import PyMongo
import lxml.html as html
from datetime import datetime, timedelta
from passlib.hash import sha512_crypt as sha512
from flask_socketio import SocketIO, send
import time
app = Flask(__name__)
conectionurl="mongodb+srv://adpac:r6mNZbEixXJUQoq0@noticias.zdgga.mongodb.net/Noticias?retryWrites=true&w=majority"
CORS(app, support_credentials=True)
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
	time.sleep(120)
	import Noticia
	Noticia.cargartodaslaspaginas()
tarea=threading.Thread(target=scrapingnoticias).start()
@app.route('/users',methods=['POST'])
def create_user():
	return{'message':'received'}

@app.route('/')
def home():
	print(__name__)
	print("redireccionado")
	rol="ninguno"
	if session.get("user")!=None:
		rol=session.get("type")
		
		print(rol)
	noticias=db.noticia
	listapaginanoticias=list(db.Paginanoticias.find({},{"URLPrincipal":1,"_id":0}))
	Noti =list(noticias.find().sort("fechaasig",-1).limit(20))
	hoy=datetime.today()
	ayer=hoy-timedelta(days=1)
	portada=list(noticias.find({'estiular':True, 'fecharecup':{'$lt': hoy, '$gte': ayer}}).sort("fechaasig",-1).limit(20))
	listacategorias=list(db.Categoria.find({}))
	Noticiascat=list(noticias.find({"categoriaprin":"6283257b2964b7cbd0b5a9ab"}).sort("fechaasig",-1).limit(20))
	noticiaspagina=[]
	if len(listapaginanoticias)>0:
		urlfuente=listapaginanoticias[0]["URLPrincipal"]
		if urlfuente[-1:]=="/":
			urlfuente=urlfuente[0:-1]
		noticiaspagina=list(noticias.find({"urlfuente": urlfuente}).sort("fechaasig",-1).limit(20))
	print(noticiaspagina)

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
			print(contraseña)
			print("passcod", passcod)
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
				return redirect(url_for('iniciarsesion'))
		else:
			mensaje="Usuario no valido"
			print(mensaje)
			return redirect(url_for('iniciarsesion'))

	
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
	return render_template('home.html')
	


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
	listaenlaces=scr.obtenerenlaces(urlprincipal,xpathcabecera)
	print(listaenlaces)
	response=make_response(render_template('formpart2.html', xpathcabecera=xpathcabecera, xpathtitular=xpathtitular, urlprincipal=urlprincipal, lista=listaenlaces, listacategorias=listacategorias))
	print(urlprincipal)
	response.set_cookie('Urlprincipal',urlprincipal)
	response.set_cookie('Xpathtitular',xpathtitular)
	response.set_cookie('Xpathcabecera',xpathcabecera)
	return response





@app.route('/formpart3', methods=['POST'])
@cross_origin(origin='*')
def formpart3():
	#https://www.la-razon.com/nacional/
	#https://erbol.com.bo/nacional
	#https://www.eldiario.net/portal/category/nacional/
	#https://www.paginasiete.bo/nacional/
	url="https://www.paginasiete.bo/nacional/"
	urlp="https://www.paginasiete.bo"
	listaurls=[]
	listacategoria=[]
	if(request.method=="POST"):
		url=request.form["campo1"]
		numsuburls=request.form["numurls"]
		for i in range(1, int(numsuburls)):
			suburl=request.form["campo"+str(i)]
			categoriaurl=request.form["cat"+str(i)]
			listaurls.append(suburl)
			listacategoria.append(categoriaurl)
		urlp=request.cookies.get("Urlprincipal")
		texto=scr.cargarpaginaycorregir(url,urlp)

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
	
	response=make_response(render_template('xpathselector.html', debug=True, url=url, texto=dochtml))
	response.set_cookie("listasuburls",json.dumps(listaurls))
	response.set_cookie("listacategorias",json.dumps(listacategoria))
	return response

@app.route('/formpart4', methods=['POST'])
def formpart4():
	xpathurlsnoticias=""
	xpathsiguiente=""
	tipopagina=""
	if request.method=='POST':
		xpathurlsnoticias=request.form["xpathenlace"]
		xpathsiguiente=request.form["xpathsiguiente"]
		tipopagina=request.form["tipopagina"]
		print("xpsig: ",xpathsiguiente)
	urlp=request.cookies.get("Urlprincipal")

	xpathnoticia=request.cookies.get("Xpathtitular")
	print(urlp)
	print(xpathsiguiente)
	#urlnoticia,textourl=scr.consultarxpa(urlp,xpathnoticia)
	urlnoticia=scr.obtenerenlaces(urlp,xpathnoticia)
	print("34234234")
	print(xpathnoticia)
	print(urlnoticia)
	url=urlnoticia[0]
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
	response=make_response(render_template('xpathselectornoticias.html', debug=True, url=url, texto=dochtml))
	response.set_cookie("xpathurlnoticias",xpathurlsnoticias)
	response.set_cookie("xpathsiguiente",xpathsiguiente)
	response.set_cookie("tipopagina",tipopagina)
	return response
	


@app.route('/agregar')
#Redireccion para agregar pagina
def agregar():

	return render_template('agregar.html',title="agregar")

@app.route('/evaluarpag', methods=['GET', 'POST'])
#al momento de agregar la nueva pagina llenaremos un formulario para identificar los patrones de la misma
def evaluarpag():
	direccion="evaluarpag.html"
	documento=""
	
	if request.method=='POST':
		url=request.form['urlpaginanoticia']

		texto=scr.cargarpaginaycorregir(url,url)
		css='<link rel="stylesheet" type="text/css" media="screen" href="/static/css/cssxpathnoticias.css">'
		iniciobody=re.search("<body.*>",texto)
		iniciohead=re.search("<head.*>",texto)

		parte1=texto[0:iniciohead.end()]
		parte2=texto[iniciohead.end():iniciobody.end()]
		parte3=texto[iniciobody.end():]
		documento=css+parte1+parte2+parte3

	return render_template(direccion, title="evaluarpag", url=url, texto=documento)

@app.route('/agregarpatrones', methods=['GET', 'POST'])
def agregarpatrones():
	direccion="agregarpatrones.html"
	pagina=""
	if request.method=='POST':
		dominioprincipal=request.form['urlP']
		urlsseleccionadas=[] #SubUrl
	
		contini=[] #contador inicial de las URLs
		contfin=[] #contafor final de las urls
		numero=request.form['numurls']
		paginacion=""
		for i in range(1, int(numero)):
			rurl="campo"+str(i)
			print(rurl)
			print("------------------")
			url=request.form[rurl]
			urlsseleccionadas.append(url)
			pag, ini, fin =scr.obtenernumeracionpag(url)
			print("Paginacion: ", pag)
			paginacion=pag
			contini.append(ini)
			contfin.append(fin)
		print('Hola a todos')
		
	return render_template(direccion, title="agregarpatrones", urlsel=urlsseleccionadas, paginacion=paginacion, ini=contini, fin=contfin,dp=dominioprincipal)


@app.route("/subirpagina", methods=["POST"])
def subirpagina():
	if request.method=='POST':
		paginaprincipal=request.cookies.get("Urlprincipal")
		xpathcabecera=request.cookies.get("Xpathcabecera")
		xpurlnoticiaprincipal=request.cookies.get("Xpathtitular")
		listaurlcategorias=request.cookies.get("listasuburls")
		listacategorias=request.cookies.get("listacategorias")
		xpathurlnoticias=request.cookies.get("xpathurlnoticias")
		xpathpagsig=request.cookies.get("xpathsiguiente")
		tipopagina=request.cookies.get("tipopagina")
		#xpath de las noticias
		xptitularnot=request.form['input1']
		xpresumennot=request.form['input2']
		xpimgnot=request.form['input3']
		xpdesimgnot=request.form['input4']
		xpvideonot=request.form['input5']
		xpdesvideonot=request.form['input6']
		xpredactornot=request.form['input7']
		xpfechanot=request.form['input8']
		xpparrafos=request.form['input9']
		xpcategoriasnot=request.form['input10']
		#Añadimos los datos a la base de datos de MongoDb (coleccion Paginanoticias)
		colpagina={
			"URLPrincipal":paginaprincipal,
			"urls":listaurlcategorias,
			"categorias":listacategorias,
			"Xpathcabecera":xpathcabecera,
			"Xpathnotprincipal":xpurlnoticiaprincipal,
			"Xpathurlsnoticias":xpathurlnoticias,
			"Xpathpagsig":xpathpagsig,
			"Tipo":tipopagina,
			"datosnoticia":{
				"xptitular":xptitularnot,
				"xpresumen":xpresumennot,
				"xpredactor":xpredactornot,
				"xpfecha":xpfechanot,
				"xpimagen":xpimgnot,
				"xpdesimagen":xpdesimgnot,
				"xpparrafos":xpparrafos,
				"xpvideo":xpvideonot,
				"xpdesvideo":xpdesvideonot,
				"xpcategorias":xpcategoriasnot
			}
		
		}
		colpaginanoticia=db['Paginanoticias']
		colpaginanoticia.insert_one(colpagina)


		
		
	mensaje="Se añadio la pagina web con exito "
	mensajesec=mensajesec="A partir de ahora se empezara recolectar noticias de esta paginaweb "+paginaprincipal
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
@app.route("/ajaxpaginanoticia", methods=["POST"])
def ajaxpaginanoticia():
	paginaprincipal= request.form['urlpaginanoticia']
	print("-------------")
	print(paginaprincipal)
	urls=scr.obtenerurlsec(paginaprincipal)
	paginahtml=scr.cargarpaginaweb(paginaprincipal,  paginaprincipal)
	print(urls)
	response={
		'status': 200,
		'url': str(paginaprincipal),
		'Paginahtml':str(paginahtml),
		'urlssec':urls,
		'id': 1
	}
	return json.dumps(response)
@app.route("/ajaxcategorias", methods=["POST"])
def ajaxcategorias():
	categoria=request.form['categoria']
	noticias=db.noticia	
	cat=str(categoria)
	print("Categoria: ",cat)
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
	print("Categoria: ",cat)
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
	print("Añadido: ",insertar.inserted_id)
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
	print(textosinsw)
	Noti =list(dbnoticias.find({"$text": {"$search": textosinsw}, "urlnoticia":{"$ne":url} }, { "score": { "$meta": "textScore" }}).sort([('score', {'$meta': 'textScore'})]).limit(10))
	response={
		'status': 200,
		'Noticias':dumps(Noti),
		'id': 1
	}
	return json.dumps(response)
if __name__ == '__main__':
	app.run()
	socketio.run(app,debug=True, port=5004)

	
