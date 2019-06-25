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
    contenedores = page_soup.findAll("div",{"class":"lista-moto"})
    contenedor = contenedores[0]  #Esta linea no la estas usando la sobreescribes mas adelante 

    # Guardamos la data en una lista para poder usarala luego
    motos=[]
    for contenedor in contenedores:
    # Nombre y cilindrada de la moto
        nombre_moto = contenedor.findAll("h2",{"class":"tittle"})
        nombre = nombre_moto[0].text
    # Precio de la moto
        precio_moto = contenedor.findAll("div",{"class":"price"})[0].text
        mini = contenedor.findAll("div",{"class":"price_mini"})[0].text

        precio_lista, precio_contado, precio_promo = get_precios(precio_moto, mini)

        # cada moto es un diccionario, y esta es una lista de diccionarios
        motos.append({
            'moto':nombre,
            'precio_lista' : precio_lista,
            'precio_contado' : precio_contado,
            'precio_promo' : precio_promo
            })
    # Se retorna la lista
    return motos

def get_precios(p, pm):
    ''' Funcion que indentifica que tipo en que campo se encuentra el precio especifico'''
    lis = "LISTA"
    con = "CONTADO"
    pro = "PROMO"

    p_lista = p if p.find(lis) > -1 else (pm if  pm.find(lis) > -1 else '')
    lista = clean_price(p_lista)

    p_contado = p if p.find(con) > -1 else (pm if  pm.find(con) > -1 else '')
    contado = clean_price(p_contado)

    p_promo = p if p.find(pro) > -1 else (pm if  pm.find(pro) > -1 else '')
    promo = clean_price(p_promo)
    
    return lista,promo,contado

def clean_price(price_str):
    ''' Puncion que obtiene el numero del precio'''
    pos = price_str.find("$")+1
    nstr = price_str[pos:].strip(' ').replace('.','')
    num = int(nstr) if nstr != '' else 0 
    return num


def imprimir_dato(dic):
    '''funcion para implimir recibe un diccionario'''
    # Puedes implimirlo como lo tenias antes asi
    # print("moto: " + dic['moto']) 
    # print("precio: " + dic['precio'])

    print('~'*20)
    # o puedes)imprimir el diccionario completo
    print(dic)


def escribir_achivo(motos):
    '''esta funcion recibe un diccionario'''
    # filename = "motos.csv" Estamos declaransola como una constante global

    # siempre que puedas usa "with" sirve para cerrar el archivo automaricamente
    with open(OUT_FILE, 'w') as f:
        # El modulo de CSV tiene un metodo para escribir archivos diccionarios, recibe los cambios como una lista

        cantidad = len(motos)
        escritor = csv.DictWriter(f,fieldnames=['moto', 'precio_lista', 'precio_contado','precio_promo'])
        escritor.writeheader()
        for moto in motos:
            escritor.writerow(moto)
            imprimir_dato(moto)

    return f"Escrito con Exito {cantidad} registros"
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

