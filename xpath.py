
from requestshtml import HTMLSession
import requestshtml
import asyncio
def cargarpaginarapida(urlpagina):
    s = requestshtml.HTMLSession()
    r=s.get(urlpagina)
    r.html.render(timeout="60")
    respuesta=r.html.xpath("//a")
    r.session.close()
    r.close()
    print(respuesta)
    return respuesta



cargarpaginarapida("http://www.elalteno.com.bo/")