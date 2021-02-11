#ejercicios/ejercicio2.py

def Burbuja(l):
    for n in range(len(l)-1,0,-1):
        for i in range(n):
            if l[i]>n[i+1]:
                l[i], l[i+1] = l[i+1], l[i]

def Mezcla(l):
    p, izda, der, resul = 0,0,0,0

    if len(l) <= 1:
        return l
    else:
        mita = len(l)/2

def seleccion(l):
    for i in range(len(l)):
        for j in range(i, len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]

def Montículos(l):
    pass

