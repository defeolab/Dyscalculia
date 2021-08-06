# import socket
# from client_handler import ClientHandler
# from db.db_connector import DBConnector
from dummy_trial_matrix import generate_random_trial_matrix

# ServerSocket = socket.socket()
# DB = DBConnector()
host = '127.0.0.1'
port = 65432
# ThreadCount = 0
# try:
#     ServerSocket.bind((host, port))
# except socket.error as e:
#     print(str(e))

# print('Waiting for a Connection..')
# ServerSocket.listen(5)

while True:
    # Client, address = ServerSocket.accept()
    # print('Connected to: ' + address[0] + ':' + str(address[1]))
    # player_id = DB.get_player(address[0])
    # if player_id == - 1:
    #    player_id = DB.add_player(address[0])
    trials_matrix = generate_random_trial_matrix();
    print(trials_matrix)
    # thread = DummyClientHandler(Client, player_id, trials_matrix)
    # thread = ClientHandler(Client, DB, player_id)
    # thread.start()
    # ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
# DB.close()
# ServerSocket.close()