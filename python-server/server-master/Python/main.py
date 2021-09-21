"""
Created on Tue Aug 10 10:30:57 2021

@author: oyekp
"""
import socket
from db.db_connector import DBConnector
from server import Client_Choice
from mapping_matrix import matrix_on_indicator

ServerSocket = socket.socket()
DB = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0

# 1 means REAL, 0 means DUMMY
flag = 0 

# 1 means matrix_circle_radius(), 2 means matrix_size_chickens(), 
# 3 means matrix_space_between()
indicator = 3

# COMMENTO SU I VARI INDICATORS E I PLOT CHE OTTENGO
# Il risultato miglione lo ottengo con indicator = 3, questo perchè space between
# assume dei valori che sono lontani gli uni dagli altri, mentre circle radius
# e size chicken non li faccio "crescere" così tanto.
# Per quanto riguarda il # di chickens, non sono riuscita a ottenere un risultato
# buono, ma questo probabilmente perchè non posso assegnare valori troppo alti
# a tale parametro, o meglio potrei ma non entrerebbero nel recinto. Comunque
# giusto per fare una prova con valori alti vedere sempre indicator = 3 
# --> prova fatta (init = 5, crescita a +3) e fallita, meno valori vengono esplorati

if flag == 1:
    
# area_1_circle_radius=array[0], area_2_circle_radius=array[1], area_1_size_of_chicken=array[2], 
# area_2_size_of_chicken=array[3], area_1_average_space_between=array[4], 
# area_2_average_space_between=array[5], area_1_number_of_chickens=array[6], 
# area_2_number_of_chickens=array[7], chicken_show_time=array[8], max_trial_time=array[9]
    
    trials_matrix = [[1.4, 1.7, 1.6, 1.8, 1.4, 1.4, 3, 4, 4, 10],
                     [1.4, 1.2, 1.6, 1.3, 1.4, 1.4, 5, 2, 2, 10]]

else:
    trials_matrix = matrix_on_indicator(indicator)

game = Client_Choice(trials_matrix)
response_vector = game.run(flag, indicator, ServerSocket, host, port, DB, ThreadCount)
print ('MAIN Response Vector: ' + str(response_vector))