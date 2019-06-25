from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
my_url = 'http://www.unomotos.com.ar/'

# abrir conexión, agarrar la página req
uClient = ureq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# Agarra cada grupo de producto
contenedores = page_soup.findAll("div",{"class":"module sombra"})
contenedor = contenedores[0]

filename = "motos.csv"
f = open(filename, "w")

headers = "nombre, precio\n"

f.write(headers)

for contenedor in contenedores:
# Nombre y cilindrada de la moto
    nombre_moto = contenedor.findAll("h2",{"class":"tittle"})
    nombre = nombre_moto[0].text
# Precio de la moto
    precio_moto = contenedor.findAll("div",{"class":"price"})
    precio = precio_moto[0].text

    print("nombre: " + nombre)
    print("precio: " + precio)

    f.write(nombre + "," + precio + "\n")

f.close()
