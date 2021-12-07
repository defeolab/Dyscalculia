import socket
from db.db_connector import DBConnector
from server import Create_Game
from mapping_matrix import dummy_matrix_generator

ServerSocket = socket.socket()
DB = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0

# 1 means SIMULATED, 0 means REAL
# simulation_on (da modificare con flag) --> FATTO
simulation_on = 1

# Non-Numerical variable selection (at the moment, we select just one of them)
nnd_selector = 3

# REAL GAME
if simulation_on == 0:
    
    # The trials_matrix is composed by a number of rows, in which every row 
    # represents a single trial. Each column of the matrix expresses a "double" 
    # information, since, if a first column gives us that data for the left area, 
    # the following column gives us the same data but for the right area,
    # except for the last two columns, which are described down below.
    # The single trial contains 10 fields:
        # --> First and second columns are called area_1_circle_radius and
        # area_2_circle_radius and those define the circle radius of both areas
        # --> Third and fourth columns are called area_1_size_of_chicken and
        # area_2_size_of_chicken, so define how big the chicken must be in that area
        # --> Fifth and sixth columns are called area_1_average_space_between and
        # area_2_average_space_between, define the space that separes one chicken 
        # by another one, on average, in each area
        # --> Seventh and eighth colums are called area_1_number_of_chickens and
        # area_2_number_of_chickens, which tells us how many chickens must be showed
        # in each area
        # --> Nineth column is called chicken_show_time, indicates how long the 
        # chickens are shown on the screen
        # --> Tenth column is called max_trial_time and defines the total duration 
        # of the game / trial

        # COSE DA EVOLVERE:
            # 1. anche l'ev del gioco reale deve essere automatica, questo è solo all'inizio
            # in seguito la 'computazione' della matrice sarà tutta fatta dall'IA
            # 2. scegliere NND e cambiando quella cambieranno tutte le variabili
        
        # Example of trials_matrix, can be changed
    
    trials_matrix = [[1.4, 1.2, 10, 4, 3, 15, 2, 15, 2, 10],
        [1.4, 1.2, 4, 10, 0.9, 3, 15, 2, 2, 10]]

# SIMULATED GAME 
else:
    trials_matrix = dummy_matrix_generator(nnd_selector)

game = Create_Game(trials_matrix)
response_vector = game.run(simulation_on, nnd_selector, ServerSocket, host, port, DB, ThreadCount)

print('MAIN Response Vector: ' + str(response_vector))
print(len(response_vector))