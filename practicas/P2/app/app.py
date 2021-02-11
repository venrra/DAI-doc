#./app/app.py
from flask import Flask, render_template
app = Flask(__name__)
from ejercicios import ejerciciosP1
import random
from random import randrange as r

@app.route('/')
def hello_world():
    return render_template('base.html')

""" @app.route('/')
def index():
    f = open("./static/direcciones.html", "r")
    index = f.read()
    f.close()
    return index """

 # ejercicio 2
@app.route('/ordenacion_burbura/<l>')
def ordenacion_burbura(l):
    lista=list(l)
    for i in range(len(lista)):
        if ' ' in lista:
            lista.remove(' ')
    return ejerciciosP1.Burbuja(lista)

# ejercicio 2
@app.route('/ordenacion_seleccion/<l>')
def ordenacion_seleccion(l):
    lista=list(l)
    for i in range(len(lista)):
        if ' ' in lista:
            lista.remove(' ')
    return ejerciciosP1.Burbuja(lista)

# ejerccio 3
@app.route('/criba/<num>')
def criba(num):
    return ejerciciosP1.criba(int(num))

# ejerccio 4
@app.route('/fibo')
def fibo():
    return ejerciciosP1.ejercicio4()

# ejerccio 5
@app.route('/corchetes/<num>')
def corchetes(num):
    return ejerciciosP1.corchetes(int(num))

# ejerccio 6
@app.route('/expresiones/<cadena>')
def expresiones(cadena):
    return ejerciciosP1.expresiones(cadena)


# subir nota
def escribe_cabecera(s):
    s = '''<!DOCTYPE html>
                <html>
                <html lang="en">
                <head>
                    <meta charset='utf-8'>
                    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                    <title>SVG Dinamico</title>
                    <meta name='viewport' content='width=device-width, initial-scale=1'>
                    <link rel='stylesheet' type='text/css' media='screen' href='main.css'>
                    <script src='main.js'></script>
                </head>
                <body>
                    <body>
                        <div>'''+ s +"</div></body></html>"
    return s
@app.route('/svg')
def svg_dinamico():

    color = lambda: '#'+''.join(['abcdef1234567890'[r(15)] for _ in range(6)])
    html = "<svg width='700' height='700'>"
    html += "<rect height='700' width='700' fill='%s'/>" %(color())
    for i in range(20):
        ANCHO = random.randrange(700)
        ALTO = random.randrange(700)
        forma = r(3)
        # lineas
        if forma==0:
            puntos = ""
            for _ in range(r(20)):
                puntos = str(r(700)) + " " + str(r(700))+", "
            html += "<polyline points='" + puntos + "' "
            html += "fill='none' stroke-width='2' stroke='"+ str(color()) + "' fill-opacity='1.0' />"
        # circulos
        elif forma==1:
            html += "<circle cx='" + str(ANCHO) + "'" + " Cy='"+str(ALTO)+"'" + "r='"+ str(r(1+int(min(ALTO, ANCHO)/4))) + "' "
            html += "fill='"+ str(color()) +"' fill-opacity='1.0' />"
        # rectangulos
        else:
            html += "<rect x='" + str(ANCHO) + "'" + " y='"+str(ALTO)+"'" + " width='"+str(ANCHO/2)+"' height='" + str(ALTO/2)+"' "
            html += "fill='"+ str(color()) +"' fill-opacity='0.5' />"

    html += "</svg>"

    s = escribe_cabecera(html)
    return s

@app.errorhandler(404)
def page_not_found(error):
    return "<H1 align=\"center\">Donde vas tuuu 404</H1>", 404