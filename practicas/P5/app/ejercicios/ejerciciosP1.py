#ejercicios/ejerciciosP1.py

import os
import re
import random

#-------------------ejercicio 2--------------------------------------
def Burbuja(l):
    for n in range(len(l)-1,0,-1):
        for i in range(n):
            if l[i]>l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]
    return l.__str__()

def seleccion(l):
    for i in range(len(l)):
        for j in range(i, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]
    return l.__str__()


# -------------------ejercicio3--------------------------------------
def criba(num):
    conjunto = list(range(2,num+1))
    for primo_actual in conjunto:
        cont=2
        while cont*primo_actual < num:
            if conjunto.count(cont*primo_actual) != 0: conjunto.remove(cont*primo_actual)
            cont+=1
    return conjunto.__str__()

# -------------------ejercicio 4--------------------------------------
def ejercicio4():
    inpu = open("./ejercicios/file")
    output = open('./ejercicios/resul', 'w')

    cont = int(inpu.readline())

    N0 = 0
    N1 = 1
    for i in range(cont):
        Nn = N0 + N1
        N0 = N1
        N1 = Nn

    output.write(Nn.__str__())

    s = "Archivo de entrada: " + cont.__str__() + " Archivo de salida: " + Nn.__str__()

    inpu.close()
    output.close()

    return s


# -------------------ejercicio 5--------------------------------------

def corchetes(num):
    conjunto = ['[', ']']

    cadena = random.choices(conjunto, k=random.randint(1,num))

    cont = 0
    for x in cadena:
        if cont < 0: break
        if x == '[':
            cont+=1
        else:
            cont-=1

    s = "La cadena de corchetes: " + cadena.__str__() + " es: "

    if cont:
        s += "INCORRECTA"
    else:
        s += "CORRECTA"
    return s

# -------------------ejercicio 6--------------------------------------
import re
def expresiones(cadena):
    # Identificar cualquier palabra seguida de un espacio
    match1 = re.search(r'(^[^ ]+ [A-Z]$)' , cadena)
    # Identificar correos electrónicos válidos
    match2 = re.search(r'(^\S\D[\w\.\S]+)@([\w\.]+)(\.[\D\w]{1,3}$)\b' , cadena)
    # Identificar números de tarjeta de crédito
    match3 = re.search(r'^[\d]{4}(\-|\ )[\d]{4}(\-|\ )[\d]{4}(\-|\ )[\d]{4}$' , cadena)

    if match1:
        s = "Identificado cualquier palabra seguida de un espacio y una mayuscula"
    elif match2:
        s = "Correo electronico valido"
    elif match3:
        s = "Targeta de credito valida"
    else:
        s = "No coincide con nada"

    return s

print(Burbuja([9,7,6,5,4]))
print(seleccion([9,7,6,5,4]))
print(criba(50))
print(ejercicio4())
print(corchetes(10))
