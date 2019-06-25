from variables import MY_URL, OUT_FILE

from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

# Python tiene un modulo para CSV
import csv

def agarrar_pagina():
    # abrir conexión, agarrar la página ureq
    uClient = ureq(MY_URL)
    page_html = uClient.read()
    uClient.close()
    # Se retorna el string 
    return page_html

def select_producto(html):
    # html parsing
    page_soup = soup(html, "html.parser")

    # Agarra cada grupo de producto
    contenedores = page_soup.findAll("div",{"class":"module sombra"})
    contenedor = contenedores[0]  #Esta linea no la estas usando la sobreescribes mas adelante 

    # Guardamos la data en una lista para poder usarala luego
    motos=[]
    for contenedor in contenedores:
    # Nombre y cilindrada de la moto
        nombre_moto = contenedor.findAll("h2",{"class":"tittle"})
        nombre = nombre_moto[0].text
    # Precio de la moto
        precio_moto = contenedor.findAll("div",{"class":"price"})
        precio = precio_moto[0].text

        # cada moto es un diccionario, y esta es una lista de diccionarios
        motos.append({'moto':nombre, 'precio':precio})

    # Se retorna la lista
    return motos

def imprimir_dato(dic):
    '''funcion para implimir recibe un diccionario'''
    # Puedes implimirlo como lo tenias antes asi
    print("moto: " + dic['moto']) 
    print("precio: " + dic['precio'])

    print('~'*20)
    # o puedes)imprimir el diccionario completo
    print(dic)


def escribir_achivo(motos):
    '''esta funcion recibe un diccionario'''
    # filename = "motos.csv" Estamos declaransola como una constante global

    # siempre que puedas usa "with" sirve para cerrar el archivo automaricamente
    with open(OUT_FILE, 'w') as f:
        # El modulo de CSV tiene un metodo para escribir archivos diccionarios, recibe los cambios como una lista

        escritor = csv.DictWriter(f,fieldnames=['moto', 'precio'])
        escritor.writeheader()
        for moto in motos:
            escritor.writerow(moto)
            imprimir_dato(moto)

    return "Escrito con Exito"
''' La aplicación debe tener un solo punto de entrada, 
ese sera la funcion Main donde se ejecuta todo
Todo el codigo se organiza en funciones para hacerlo mas
modular y reutilizable
'''
def main():
    # Aqui tienes toda la ejecución de la app
     pagina = agarrar_pagina()
     motos = select_producto(pagina)
     print(escribir_achivo(motos))


# Punto de entrada
if __name__ == '__main__':
    main()

