
"""from socketIO_client import SocketIO, LoggingNamespace
import json
socketIO = SocketIO('https://heroku-socketio-test.herokuapp.com/',5000, LoggingNamespace)
print("conectado: ",socketIO)
def enviarmensaje(mensaje):
    socketIO.emit('message',mensaje)
    socketIO.wait(seconds=1)


jsonmen={"urlprin": "https://erbol.com.bo", "url": "https://erbol.com.bo",   "categoria": "NACIONAL", "titular": "Rub\u00e9n Costas: Est\u00e1n allanado el camino para que el MAS ingrese a paso de parada en Santa Cruz", "parrafo": "\nEl exgobernador de Santa Cruz Rub\u00e9n Costas advirti\u00f3 un proceso de debilitamiento de las instituciones cruce\u00f1as y cree que la denuncia de Luis Fernando Camacho por la supuesta \u201cpublicidad fantasma\u201d est\u00e1 allanando el camino para que el MAS ingrese a paso de parada a Santa Cruz, el \u00faltimo reducto de la resistencia democr\u00e1tica.\nCostas fue nuevamente citado a una audiencia de medidas cautelares para el pr\u00f3ximo 27 de abril y la Fiscal\u00eda habr\u00eda pedido la detenci\u00f3n preventiva por 180 d\u00edas en la c\u00e1rcel de Palmasola para el exgobernador, su secretario general Rolando Aguilera y el \u00fanico concejal de su partido Dem\u00f3cratas, Manuel \u201cMamem\u201d Saavedra.\n\u201cYa las armas est\u00e1n apuntadas y definidas para matarme civilmente como es el mandato de este se\u00f1or, que no queden cenizas de Rub\u00e9n Costas ni de Dem\u00f3cratas y lo que estamos viviendo es un debilitamiento de las instituciones cruce\u00f1as que era la \u00faltima vanguardia de la resistencia democr\u00e1tica en Santa Cruz\u201d, declar\u00f3 seg\u00fan despacho de la corresponsal de Erbol-Santa Cruz Mercedes Fern\u00e1ndez.\nLa nueva citaci\u00f3n cautelar es la quinta que recibe el exgobernador cruce\u00f1o, quien asegura que \u201cest\u00e1n allanando el camino del MAS. Yo creo que si el MAS no entra hoy a Santa Cruz a paso de parada es porque simplemente tienen ellos entuertos muy graves\u201d.\nLament\u00f3 que a ra\u00edz de este proceso se cause divisi\u00f3n entre los cruce\u00f1os, mientras se observa una desacreditaci\u00f3n de la institucionalidad cruce\u00f1a y \u201ceso es la otra consigna y persecuci\u00f3n: enfrentarnos entre nosotros\u201d.\n\u201cSabemos qui\u00e9n es el estratega de esto, sabemos qui\u00e9n es el gur\u00fa, ha sido denunciado por propios y extra\u00f1os. \u00bfA qui\u00e9n responde este se\u00f1or? eso lo sabemos. \u00a0Lo lamentable es que est\u00e1 logrando su prop\u00f3sito y eso es lo triste para Santa Cruz\u201d, declar\u00f3 Costas, jefe pol\u00edtico del partido de los Verdes luego transformado en Dem\u00f3cratas que sufri\u00f3 profundas divisiones internas antes y despu\u00e9s de las elecciones generales de 2019 y 2020.", "imagen": "https://erbol.com.bo/sites/default/files/ruben_costas_0.jpg", "mensaje": "nueva noticia"}
mensaje=json.dumps(jsonmen)
enviarmensaje(mensaje)"""
import socketio
import json
sio = socketio.Client()
@sio.event
def connect():
    print('connection established')


@sio.event
def message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')

def enviarmensaje(mensaje):
    sio.emit('message',mensaje)
    sio.wait(seconds=1)
try:
    sio.connect('https://webscrapingproyecto.herokuapp.com/')
except:
    print("no se pudo conectar")
#jsonmen={"urlprin": "https://erbol.com.bo", "url": "https://erbol.com.bo",   "categoria": "NACIONAL", "titular": "Rub\u00e9n Costas: Est\u00e1n allanado el camino para que el MAS ingrese a paso de parada en Santa Cruz", "parrafo": "\nEl exgobernador de Santa Cruz Rub\u00e9n Costas advirti\u00f3 un proceso de debilitamiento de las instituciones cruce\u00f1as y cree que la denuncia de Luis Fernando Camacho por la supuesta \u201cpublicidad fantasma\u201d est\u00e1 allanando el camino para que el MAS ingrese a paso de parada a Santa Cruz, el \u00faltimo reducto de la resistencia democr\u00e1tica.\nCostas fue nuevamente citado a una audiencia de medidas cautelares para el pr\u00f3ximo 27 de abril y la Fiscal\u00eda habr\u00eda pedido la detenci\u00f3n preventiva por 180 d\u00edas en la c\u00e1rcel de Palmasola para el exgobernador, su secretario general Rolando Aguilera y el \u00fanico concejal de su partido Dem\u00f3cratas, Manuel \u201cMamem\u201d Saavedra.\n\u201cYa las armas est\u00e1n apuntadas y definidas para matarme civilmente como es el mandato de este se\u00f1or, que no queden cenizas de Rub\u00e9n Costas ni de Dem\u00f3cratas y lo que estamos viviendo es un debilitamiento de las instituciones cruce\u00f1as que era la \u00faltima vanguardia de la resistencia democr\u00e1tica en Santa Cruz\u201d, declar\u00f3 seg\u00fan despacho de la corresponsal de Erbol-Santa Cruz Mercedes Fern\u00e1ndez.\nLa nueva citaci\u00f3n cautelar es la quinta que recibe el exgobernador cruce\u00f1o, quien asegura que \u201cest\u00e1n allanando el camino del MAS. Yo creo que si el MAS no entra hoy a Santa Cruz a paso de parada es porque simplemente tienen ellos entuertos muy graves\u201d.\nLament\u00f3 que a ra\u00edz de este proceso se cause divisi\u00f3n entre los cruce\u00f1os, mientras se observa una desacreditaci\u00f3n de la institucionalidad cruce\u00f1a y \u201ceso es la otra consigna y persecuci\u00f3n: enfrentarnos entre nosotros\u201d.\n\u201cSabemos qui\u00e9n es el estratega de esto, sabemos qui\u00e9n es el gur\u00fa, ha sido denunciado por propios y extra\u00f1os. \u00bfA qui\u00e9n responde este se\u00f1or? eso lo sabemos. \u00a0Lo lamentable es que est\u00e1 logrando su prop\u00f3sito y eso es lo triste para Santa Cruz\u201d, declar\u00f3 Costas, jefe pol\u00edtico del partido de los Verdes luego transformado en Dem\u00f3cratas que sufri\u00f3 profundas divisiones internas antes y despu\u00e9s de las elecciones generales de 2019 y 2020.", "imagen": "https://erbol.com.bo/sites/default/files/ruben_costas_0.jpg", "mensaje": "nueva noticia"}
#mensaje=json.dumps(jsonmen)
#enviarmensaje(mensaje)
#disconnect()

