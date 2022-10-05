import socket
from db.db_connector import DBConnector
from dummy_client_handler import SimulatedClient
from server import Create_Game, GameServer
from mapping_matrix import dummy_matrix_generator
from plot_trials import PlotTrials
from transform_matrix import TransformMatrix

server_socket = socket.socket()
db = DBConnector()
host = '127.0.0.1'
port = 65432
ThreadCount = 0

# simulation_on is a flag that indicated if the game is a simulated one or not
# 1 means SIMULATED, 0 means REAL
simulation_on = 1

# Non-Numerical variable selection (at the moment, we select just one of them)
# Can be Either Field Area (nnd_selector = 1) or Item Surface Area (nnd_selector = 2)
nnd_selector = 1

# It controls the number of trials that will be computed by the Dummy, which will
# be equal to the nnd_number elevated to 4.
nnd_number = 5

# Alpha is the angle used for the Filtering analysis, calculated from the positive y-axis
alpha = 20

# Sigma is the parameter that specifies how big the Gaussian bell must be. It is
# used when computing the Sharpening effect
sigma = 0.5

# nnd_general is a flag: if it setted, then all the NND variables are
# automatically generated
nnd_general = 0

# # REAL GAME
# if simulation_on == 0:
    
#     # The trials_matrix is composed by a number of rows, in which every row 
#     # represents a single trial. Each column of the matrix expresses a "double" 
#     # information, since, if a first column gives us that data for the left area, 
#     # the following column gives us the same data but for the right area,
#     # except for the last two columns, which are described down below.
#     # The single trial contains 10 fields:
        
#         # --> First and second columns are called area_1_number_of_chickens and
#         # area_2_number_of_chickens, which tells us how many chickens must be showed
#         # in each area
        
#         # --> Third and fourth columns are called area_1_field_area and
#         # area_2_field_area: the field area, also known as FA, is defined as 
#         # the portion of the space where dots actually fall into
        
#         # --> Fifth and sixth columns are called area_1_item_surface_area and
#         # area_2_item_surface_area, defined as the area (in terms of number of 
#         # pixels) occupied by a single chicken
        
#         # --> Seventh column is called chicken_show_time, indicates how long the 
#         # chickens are shown on the screen
        
#         # --> Eighth column is called max_trial_time and defines the total duration 
#         # of the game / trial
    
#     trials_matrix_original = [[5, 6, 27777.78, 37777.78, 273.13, 173.13, 4, 8],
#                               [7, 6, 27777.78, 27777.78, 173.13, 173.13, 4, 8],
#                               [2, 7, 27777.78, 27777.78, 173.13, 173.13, 4, 8]]
    
#     # To transform our parameters into the ones accepted by the real game, it is
#     # mandatory to call the TransformMatrix function to obtain the right matrix
#     trials_matrix = TransformMatrix(trials_matrix_original)

# # SIMULATED GAME 
# else:
#     trials_matrix = dummy_matrix_generator(nnd_selector, nnd_number)

if simulation_on == 0:
    game = GameServer(server_socket, host, port, db)
    game.run()
else:
    client = SimulatedClient(0.5, 0.5)
    client.run(100)

# print('MAIN Response Vector: ' + str(response_vector))
# print(len(response_vector))

# PlotTrials(response_vector, trials_matrix, alpha, nnd_selector)