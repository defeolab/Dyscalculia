# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 11:28:43 2021

@author: Client
"""

from statistics import NormalDist
import scipy

point_coordinates = [1, 1]

# Se la probabilità restituita da queste funzioni è
# < 0.5, allora il punto sarà rosso, alternativamente
# il punto sarà verde

# NODO MANCANTE: come "passo il punto" alla funzione
# NormalDist o norm? .pdf() si aspetta come argomento 
# x, quindi il punto. Il mio punto però è dato da due coordinate, 
# una x e una y. Quindi come rendo la coppia di punti un punto
# solo?

# Oppure devo calcolare la media e la deviazione standard di tutti questi
# punti assieme e passarli alla funzione per trovare la gaussiana giusta?
# Credo di no, perchè abbiamo detto che i pallini devono essere più
# rossi al centro e più verdi verso l'esterno

# pdf(x) permette di calcolare la probabilità relativa che una variabile 
# casuale X si avvicini al valore x dato.

x = NormalDist(mu=0, sigma=0.2).pdf(1)
print(x)

y = scipy.stats.norm(0, 0.2).pdf(point_coordinates)
print(y)

z = NormalDist(mu=0, sigma=0.2).pdf(point_coordinates)
print(z)
