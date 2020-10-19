#ejercicios/ejercicio2.py

import random

conjunto = ['[', ']']

cadena = random.choices(conjunto, k=random.randint(1,2))

print(cadena)

cont = 0

for x in cadena:
    if cont < 0: break
    if x == '[':
        cont+=1
    else:
        cont-=1

if cont:
    print("Incorrecto")
else:
    print("correcto")