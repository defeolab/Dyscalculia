# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:30:57 2021

@author: oyekp
"""
import socket
from db.db_connector import DBConnector
from server import Flag

ServerSocket = socket.socket()
DB = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0
flag = 0 # 1 means REAL, 0 means DUMMY


# DEFINE TRIALS_MATRIX HERE MANUALLY and pass as parameter to the RUN method
# --> 


game = Flag()
game.run(flag, ServerSocket, host, port, DB, ThreadCount)

# response_vector (it was result_array before) = game.run (params + trials_matrix)


# ANALYSIS MUST BE DONE HERE, NOT IN THE DUMMY, because it must be general, because
# it must not know if it is the dummy or the real game which is played


# NEXT --> random generation of trials in all the space
# dyscalculia factor to be added later on