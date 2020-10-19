#ejercicios/ejercicio4.py

inpu = open('file')
output = open('./resul', 'w')

cont = int(inpu.readline())

N0 = 0
N1 = 1
for i in range(cont):
    Nn = N0 + N1
    N0 = N1
    N1 = Nn

output.write(Nn.__str__())

inpu.close()
output.close()