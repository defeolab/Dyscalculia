"""
Created on Tue Aug 10 10:30:57 2021

@author: oyekp
"""
import socket
from db.db_connector import DBConnector
from server import Flag
from mapping_matrix import indicate
#from trial_util import generate_dummy_random_trial_matrix 

ServerSocket = socket.socket()
DB = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0
flag = 0 # 1 means REAL, 0 means DUMMY
indicator = 1 #1 means map_matrix_radius(), 2 means map_matrix_size(), 3 means map_matrix_space()


if flag == 1:
    trials_matrix = [[1.6, 1.8, 1.8, 1.7, 4, 10, 1], [0.5, 1.2, 1.1, 1.0, 5, 8, 0], 
                     [1.3, 1.0, 2.0, 1.0, 3, 9, 0], [0.5, 1.4, 1.1, 1.4, 3, 8, 1], 
                     [1.4, 1.4, 1.2, 2.0, 5, 8, 0], [1.4, 1.6, 1.9, 1.7, 4, 9, 0], 
                     [1.6, 1.3, 1.4, 1.6, 2, 9, 1], [0.5, 2.0, 0.6, 1.9, 2, 9, 1], 
                     [0.6, 1.1, 1.6, 1.9, 3, 9, 1], [1.8, 1.5, 1.4, 1.9, 4, 8, 1]]
else:
    trials_matrix = indicate(indicator)
    #generate_dummy_random_trial_matrix(); 

game = Flag(trials_matrix)
response_vector = game.run(flag, indicator, ServerSocket, host, port, DB, ThreadCount)
print ('Response Vector: ' + str(response_vector))