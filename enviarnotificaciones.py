
"""from socketIO_client import SocketIO, LoggingNamespace
import json
socketIO = SocketIO('https://heroku-socketio-test.herokuapp.com/',5000, LoggingNamespace)
print("conectado: ",socketIO)
def enviarmensaje(mensaje):
    socketIO.emit('message',mensaje)
    socketIO.wait(seconds=1)


jsonmen={"urlprin": "https://erbol.com.bo", "url": "https://erbol.com.bo",   "categoria": "NACIONAL", "titular": "Rub\u00e9n Costas: Est\u00e1n allanado el camino para que el MAS ingrese a paso de parada en Santa Cruz", "parrafo": "\nEl exgobernador de Santa Cruz Rub\u00e9n Costas advirti\u00f3 un proceso de debilitamiento de las instituciones cruce\u00f1as y cree que la denuncia de Luis Fernando Camacho por la supuesta \u201cpublicidad fantasma\u201d est\u00e1 allanando el camino para que el MAS ingrese a paso de parada a Santa Cruz, el \u00faltimo reducto de la resistencia democr\u00e1tica.\nCostas fue nuevamente citado a una audiencia de medidas cautelares para el pr\u00f3ximo 27 de abril y la Fiscal\u00eda habr\u00eda pedido la detenci\u00f3n preventiva por 180 d\u00edas en la c\u00e1rcel de Palmasola para el exgobernador, su secretario general Rolando Aguilera y el \u00fanico concejal de su partido Dem\u00f3cratas, Manuel \u201cMamem\u201d Saavedra.\n\u201cYa las armas est\u00e1n apuntadas y definidas para matarme civilmente como es el mandato de este se\u00f1or, que no queden cenizas de Rub\u00e9n Costas ni de Dem\u00f3cratas y lo que estamos viviendo es un debilitamiento de las instituciones cruce\u00f1as que era la \u00faltima vanguardia de la resistencia democr\u00e1tica en Santa Cruz\u201d, declar\u00f3 seg\u00fan despacho de la corresponsal de Erbol-Santa Cruz Mercedes Fern\u00e1ndez.\nLa nueva citaci\u00f3n cautelar es la quinta que recibe el exgobernador cruce\u00f1o, quien asegura que \u201cest\u00e1n allanando el camino del MAS. Yo creo que si el MAS no entra hoy a Santa Cruz a paso de parada es porque simplemente tienen ellos entuertos muy graves\u201d.\nLament\u00f3 que a ra\u00edz de este proceso se cause divisi\u00f3n entre los cruce\u00f1os, mientras se observa una desacreditaci\u00f3n de la institucionalidad cruce\u00f1a y \u201ceso es la otra consigna y persecuci\u00f3n: enfrentarnos entre nosotros\u201d.\n\u201cSabemos qui\u00e9n es el estratega de esto, sabemos qui\u00e9n es el gur\u00fa, ha sido denunciado por propios y extra\u00f1os. \u00bfA qui\u00e9n responde este se\u00f1or? eso lo sabemos. \u00a0Lo lamentable es que est\u00e1 logrando su prop\u00f3sito y eso es lo triste para Santa Cruz\u201d, declar\u00f3 Costas, jefe pol\u00edtico del partido de los Verdes luego transformado en Dem\u00f3cratas que sufri\u00f3 profundas divisiones internas antes y despu\u00e9s de las elecciones generales de 2019 y 2020.", "urlimagen": "https://erbol.com.bo/sites/default/files/ruben_costas_0.jpg", "mensaje": "nueva noticia"}
mensaje=json.dumps(jsonmen)
enviarmensaje(mensaje)"""

#Estableciendo conexion con SocketIO
import socketio
import json
sio = socketio.Client()
@sio.event
def connect():
    print('connection established')

#Envia un mensaje
@sio.event
def message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

#desconectar
@sio.event
def disconnect():
    print('disconnected from server')

#Envia mensaje al servidor 
def enviarmensaje(mensaje):
    print("enviando mensaje")
    try:
        sio.connect('https://webscrapingproyecto.herokuapp.com/')
        #sio.connect('http://localhost:5000/')
        sio.emit('message',mensaje)
        print("mensaje enviado....")
        
        sio.disconnect()
    except Exception as e:
        print("ocurrio un problema al momento de enviar notificaciones")
        print(e)
        sio.disconnect()

#jsonmen={"urlprin": "https://erbol.com.bo", "url": "https://erbol.com.bo",   "categoria": "NACIONAL", "titular": "Rub\u00e9n Costas: Est\u00e1n allanado el camino para que el MAS ingrese a paso de parada en Santa Cruz", "parrafo": "\nEl exgobernador de Santa Cruz Rub\u00e9n Costas advirti\u00f3 un proceso de debilitamiento de las instituciones cruce\u00f1as y cree que la denuncia de Luis Fernando Camacho por la supuesta \u201cpublicidad fantasma\u201d est\u00e1 allanando el camino para que el MAS ingrese a paso de parada a Santa Cruz, el \u00faltimo reducto de la resistencia democr\u00e1tica.\nCostas fue nuevamente citado a una audiencia de medidas cautelares para el pr\u00f3ximo 27 de abril y la Fiscal\u00eda habr\u00eda pedido la detenci\u00f3n preventiva por 180 d\u00edas en la c\u00e1rcel de Palmasola para el exgobernador, su secretario general Rolando Aguilera y el \u00fanico concejal de su partido Dem\u00f3cratas, Manuel \u201cMamem\u201d Saavedra.\n\u201cYa las armas est\u00e1n apuntadas y definidas para matarme civilmente como es el mandato de este se\u00f1or, que no queden cenizas de Rub\u00e9n Costas ni de Dem\u00f3cratas y lo que estamos viviendo es un debilitamiento de las instituciones cruce\u00f1as que era la \u00faltima vanguardia de la resistencia democr\u00e1tica en Santa Cruz\u201d, declar\u00f3 seg\u00fan despacho de la corresponsal de Erbol-Santa Cruz Mercedes Fern\u00e1ndez.\nLa nueva citaci\u00f3n cautelar es la quinta que recibe el exgobernador cruce\u00f1o, quien asegura que \u201cest\u00e1n allanando el camino del MAS. Yo creo que si el MAS no entra hoy a Santa Cruz a paso de parada es porque simplemente tienen ellos entuertos muy graves\u201d.\nLament\u00f3 que a ra\u00edz de este proceso se cause divisi\u00f3n entre los cruce\u00f1os, mientras se observa una desacreditaci\u00f3n de la institucionalidad cruce\u00f1a y \u201ceso es la otra consigna y persecuci\u00f3n: enfrentarnos entre nosotros\u201d.\n\u201cSabemos qui\u00e9n es el estratega de esto, sabemos qui\u00e9n es el gur\u00fa, ha sido denunciado por propios y extra\u00f1os. \u00bfA qui\u00e9n responde este se\u00f1or? eso lo sabemos. \u00a0Lo lamentable es que est\u00e1 logrando su prop\u00f3sito y eso es lo triste para Santa Cruz\u201d, declar\u00f3 Costas, jefe pol\u00edtico del partido de los Verdes luego transformado en Dem\u00f3cratas que sufri\u00f3 profundas divisiones internas antes y despu\u00e9s de las elecciones generales de 2019 y 2020.", "urlimagen": "https://erbol.com.bo/sites/default/files/ruben_costas_0.jpg", "mensaje": "nueva noticia"}
"""jsonmen={
    "_id": "62d9a8c5b6403bca6b2bd184",
    "categoria": "62d6cdb7a0322239bc7de58a",
    "desimagen": "",
    "estitular": False,
    "fecha": " 20 de  Fecha de Publicaci\u00f3n: 20 jul 2022 ",
    "fechaasig": "2022-07-21 15:28:05.194100",
    "hashtags": [
        "DEPARTAMENTO DE INFORMACI\u00d3N Y COMUNICACI\u00d3N",
        " ESTRATEGIAS COMUNICACIONALES - LA CATEDRA"
    ],
    "mensaje": "nueva noticia",
    "parrafos": "La marcha de los cocaleros que exigen el cierre del mercado paralelo de la hoja de coca en la ciudad de La Paz avanza en su tercer día rumbo a la sede de Gobierno. \n Desde la cabeza de la movilización, el presidente de Autodefensa de la Asociación Departamental de Productores de Coca (Adepcoca) de La Paz, César Apaza, habló con Correo del Sur Radio FM 90.1 y apuntó contra el Gobierno.",
    "redactor": "",
    "resumen": "Con el objetivo de reconocer el trabajo de los investigadores cient\u00edficos y motivar el desarrollo y difusi\u00f3n de la ciencia, la ma\u00f1ana de este mi\u00e9rcoles 20 de julio se realiz\u00f3 el acto de presentaci\u00f3n de revistas cient\u00edficas y reconocimiento al Comit\u00e9 de Editores de la Facultad de Ciencias Puras Naturales de la #UMSA.",
    "titular": "Desde la marcha de Adepcoca: “El Ministro nos convoca para violar normas y leyes",
    "urlfuente": "https://correodelsur.com/",
    "urlimagen": "https://correodelsur.com/img/contents/images_360/2022/09/06/b8c0e540-09ea-4db3-9bb2-b12e38ee4105.jpg",
    "urlnoticia": "https://correodelsur.com/politica/20220906_desde-la-marcha-de-adepcoca-el-ministro-nos-convoca-para-violar-normas-y-leyes.html"
}
mensaje=json.dumps(jsonmen)
enviarmensaje(mensaje)
sio.disconnect()

"""