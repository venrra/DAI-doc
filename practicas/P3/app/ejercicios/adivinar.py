import random

print("Adivina un numero entre 0-100")

numero = random.randint(0,100)
elecion = int(input())

while  elecion != numero:  
    if numero < elecion:
        print("Tu eleccion es mayor")
    else:
        print("Tu eleccion es menor")
    elecion = int(input())

print("has adivinado el numero: " + numero.__str__())