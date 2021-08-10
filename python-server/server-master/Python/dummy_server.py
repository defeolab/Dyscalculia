# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 19:02:44 2021

@author: oyekp
"""

from dummy_client_handler import generate_random_trial_matrix, DummyClientHandler

trials_matrix = generate_random_trial_matrix();
host = '127.0.0.1'
print('Connected to: ' + host)
player_id = 1
print('Player ID: ' + str(player_id))
print('SENT DATA: ' + str(trials_matrix))
print()

if player_id == 1:
    thread = DummyClientHandler(trials_matrix)
    thread.Run() 


 