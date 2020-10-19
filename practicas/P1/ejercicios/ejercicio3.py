#ejercicios/ejercicio3.py

num = int(input("introduice un numero: "))

conjunto = list(range(2,num+1))

for primo_actual in conjunto:
    cont=2
    while cont*primo_actual < num:
        if conjunto.count(cont*primo_actual) != 0: conjunto.remove(cont*primo_actual)
        cont+=1

print(conjunto)