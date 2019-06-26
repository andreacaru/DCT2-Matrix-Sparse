import numpy as np
import time
import math
from scipy.fftpack import fft, dct, idct
from PIL import Image


#matrice test
'''
test = [[231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]]

for i in range (0, 8):
    for j in range (0, 8):
        print(test[i][j])
    print("\n")
'''

#creo matrice di N elementi
N = 1
f1 = np.random.randint(255, size=(N, N))
c1 = np.zeros(shape=(N,N))

#inizializzo il tempo di esecuzione per calcolare la DCT2
start_time = time.time()

#calcolo DCT su righe
for i in range(0, N):
    for k in range(0, N):
        sum=0
        if (k == 0):
            alfa = math.sqrt(1/N)
        else:
            alfa = math.sqrt(2/N)
        for j in range(0, N):
            sum += ((f1[i][j])*(math.cos(k*math.pi*((2*j+1)/(2*N)))))
        c1[i][k] = sum * alfa

'''
print("My DCT1: ")   
for i in range (0, N):
    for j in range (0, N):
        print(c1[i][j])
    print("\n")
'''

f2 = c1
c2 = np.zeros(shape=(N,N))

#calcolo DCT su colonne
for j in range(0, N):
    for k in range(0, N):
        sum=0
        if (k == 0): 
            alfa = math.sqrt(1/N)
        else: 
            alfa = math.sqrt(2/N)
        for i in range(0, N):
            sum += ((f2[i][j])*(math.cos(k*math.pi*((2*i+1)/(2*N)))))
        c2[k][j] = sum * alfa

'''
print("My DCT2: ") 
#stampo c2 finale al solo scopo di visualizzazione
for i in range (0, N):
    for j in range (0, N):
        print(c2[i][j])
    print("\n")
'''

#stampo tempo di esecuzione della DCT2
print("--- %s seconds --- MYDCT2" % (time.time() - start_time))
print("\n")

start_time = time.time()

dct1 = dct(f1, norm='ortho')
dct2 = dct(dct1.T, norm='ortho')
dct2 = dct2.T

#print pretty matrix dct2
s = [[str(e) for e in row] for row in dct2]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print ("\n".join(table))

print("--- %s seconds --- SCIPY DCT2" % (time.time() - start_time))




