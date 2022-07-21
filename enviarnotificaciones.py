
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
jsonmen={
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
    "parrafos": "Con el objetivo de reconocer el trabajo de los investigadores cient\u00edficos y motivar el desarrollo y difusi\u00f3n de la ciencia, la ma\u00f1ana de este mi\u00e9rcoles 20 de julio se realiz\u00f3 el acto de presentaci\u00f3n de revistas cient\u00edficas y reconocimiento al Comit\u00e9 de Editores de la Facultad de Ciencias Puras Naturales de la #UMSA.En la oportunidad se entregaron reconocimientos a la Dra. M\u00f3nica Moraes de la revista \u201cEcolog\u00eda en Bolivia\u201d; Dr. Jos\u00e9 Antonio Bravo de la \u201cRevista Boliviana de Qu\u00edmica\u201d; Dr. Wilfredo Tavera de la \u201cRevista Boliviana de F\u00edsica\u201d; Dr. Jimmy Santamar\u00eda de la \u201cRevista Boliviana de Matem\u00e1tica\u201d; Lic. Emma Mancilla de la revista \u201cVarianza\u201d de Estad\u00edstica y a los universitarios: Jorge Luis Ur\u00eda, Sebasti\u00e1n Irigoyen, Ana Patricia Flores, Juan Gabriel Chac\u00f3n y Willy Daniel Ayala de la revista \u201cPura Ciencia \u2013 M\u00e1s All\u00e1 del Infinito\u201d.\ud83d\udfe5 El Rector, M.Sc. Oscar Heredia fue el encargado de entregar los reconocimientos a los docentes editores de las revistas cient\u00edficas, cuestion\u00f3 el trabajo de los gobiernos de turno para impulsar la investigaci\u00f3n y c\u00f3mo la universidad produce con las limitaciones que tiene, en esa l\u00ednea resalt\u00f3 el trabajo de la Facultad de Ciencias Puras y Naturales por su iniciativa y liderazgo para elaborar las revistas cient\u00edficas, adem\u00e1s felicit\u00f3 a los estudiantes que asumieron el desaf\u00edo de trabajar en el desarrollo de la investigaci\u00f3n.La Vicerrectora, Dra. Mar\u00eda Eugenia Garc\u00eda, resalt\u00f3 la importancia de reconocer en trabajo que permite generar conocimiento que est\u00e1 plasmado en una revista y repas\u00f3 el trabajo que se desarrolla detr\u00e1s de cada publicaci\u00f3n, las investigaciones, el proceso que implica, los resultados hasta llegar a escribir un art\u00edculo cient\u00edfico que forme parte de una revista y que han sido revisados por pares internacionales, lo que permite incrementar las redes de investigaci\u00f3n a trav\u00e9s de la visibilizaci\u00f3n.El Decano, M.Sc. Grover Rodr\u00edguez, felicit\u00f3 a los docentes editores y record\u00f3 que una de las tareas asumidas era visibilizar los trabajos de los investigadores y estudiantes de la Facultad y consolidar las revistas indexadas e impulsar al resto de las Carreras para que cuenten con estos medios de difusi\u00f3n cient\u00edfica.El Vicedecano, Dr. Jos\u00e9 Luis Vila hizo una breve presentaci\u00f3n sobre las revistas cient\u00edficas, consideradas como los principales canales de comunicaci\u00f3n y difusi\u00f3n de los resultados de investigaci\u00f3n en todos los campos del conocimiento, m\u00e1s a\u00fan cuando se trata de textos indexados que son visibilizados a nivel mundial, generando prestigio internacional para sus autores.En representaci\u00f3n de los docentes editores, el Dr. Jos\u00e9 Antonio Bravo, agradeci\u00f3 el reconocimiento y realiz\u00f3 una breve exposici\u00f3n sobre el trabajo que implica elaborar una revista cient\u00edfica, su indexaci\u00f3n y las plataformas donde estas se difunden.Actualmente la Facultad de Ciencias Puras y Naturales cuenta con las revistas indexadas de las Carreras de F\u00edsica, Biolog\u00eda y Qu\u00edmica, adem\u00e1s, actualmente se trabaja en la indexaci\u00f3n de las revistas de Matem\u00e1tica y Estad\u00edstica y la publicaci\u00f3n de la revista del Centro de Estudiantes de esta Unidad Acad\u00e9mica. En Bolivia existen actualmente 34 revistas indexadas de las cuales, diez pertenecen a la #UMSA.#UMSAcomunicacionesSIGUENOS ENUniversidad Mayor de San Andr\u00e9s@UMSAinformacionUniversidad Mayor de San Andr\u00e9sumsa.informacionCorreo InstitucionalNuestra Ubicaci\u00f3n",
    "redactor": "",
    "resumen": "Con el objetivo de reconocer el trabajo de los investigadores cient\u00edficos y motivar el desarrollo y difusi\u00f3n de la ciencia, la ma\u00f1ana de este mi\u00e9rcoles 20 de julio se realiz\u00f3 el acto de presentaci\u00f3n de revistas cient\u00edficas y reconocimiento al Comit\u00e9 de Editores de la Facultad de Ciencias Puras Naturales de la #UMSA.",
    "titular": "PRODUCCI\u00d3N Y DIVULGACI\u00d3N CIENT\u00cdFICA EN LA UMSA - Reconocimiento a revistas cient\u00edficas de Ciencias Puras y Naturales ",
    "urlfuente": "https://umsa.bo",
    "urlimagen": "/image/image_gallery?img_id=5653242",
    "urlnoticia": "https://umsa.bo/web/guest/57/-/asset_publisher/sIpuYXdbB9M8/content/20-07/20142"
}
#mensaje=json.dumps(jsonmen)
#enviarmensaje(mensaje)
#sio.disconnect()

