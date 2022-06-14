
import html5lib
import requests
from urllib.request import urlopen


def abrirpagina(urlpagina):
    document=None
    with urlopen(urlpagina) as f:
        document = html5lib.parse(f, transport_encoding=f.info().get_content_charset())
    print(document)
    return document
