#ejercicios/ejercicio6.py
# -*- coding: utf-8 -*-

import os 
import re

def menu():
    os.system("clear")
    print("Selecciona una expresion para analizar")
    print("\t1 - Identificar cualquier palabra seguida de un espacio y una única letra mayúscula")
    print("\t2 - Identificar correos electrónicos ")
    print("\t3 - tarjeta de credito con - o espacio")
    print("\t9 - salir")


# expresion 1 [\w\D]+ [A-Z]
# expresion para un correo (?!\d)\w+@\w+\.[\D\w]+  \b[\D]\w+@\w+\.[\D\w]{2,3}\b
# [\d]{4}(\-|\ )[\d]{4}(\-|\ )[\d]{4}(\-|\ )[\d]{4}