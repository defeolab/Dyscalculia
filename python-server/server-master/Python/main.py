"""
Created on Tue Aug 10 10:30:57 2021

@author: oyekp
"""
import socket
from db.db_connector import DBConnector
from server import Flag
from mapping_matrix import indicate

ServerSocket = socket.socket()
DB = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0

flag = 0 # 1 means REAL, 0 means DUMMY

# 1 means map_matrix_radius(), 2 means map_matrix_size(), 3 means map_matrix_space()
indicator = 1

if flag == 1:
    
    # Prova nuova trials_matrix. I parametri sono i seguenti: 
    
# area_1_circle_radius=array[0], area_2_circle_radius=array[1], area_1_size_of_chicken=array[2], 
# area_2_size_of_chicken=array[3], area_1_average_space_between=array[4], 
# area_2_average_space_between=array[5], area_1_number_of_chickens=array[6], 
# area_2_number_of_chickens=array[7], chicken_show_time=array[8], max_trial_time=array[9]
    
    trials_matrix = [[1.4, 1.7, 1.6, 1.8, 1.4, 1.4, 3, 4, 4, 10]]

else:
    trials_matrix = indicate(indicator)

game = Flag(trials_matrix)
response_vector = game.run(flag, indicator, ServerSocket, host, port, DB, ThreadCount)
print ('MAIN Response Vector: ' + str(response_vector))