import socket
from client_handler import ClientHandler
from dummy_client_handler import DummyClientHandler
 

class Client_Choice():
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
           
    def run(self, flag, indicator, ServerSocket, host, port, DB, ThreadCount):
        if flag == 1:
            try:
                ServerSocket.bind((host, port))
            except socket.error as e:
                print(str(e))
            
            print('Waiting for a Connection..')
            ServerSocket.listen(5)
            
            while True:
                Client, address = ServerSocket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                player_id = DB.get_player(address[0])
                if player_id == - 1:
                    player_id = DB.add_player(address[0])
                thread = ClientHandler(Client, DB, player_id, self.trials_matrix)
                response_vector = thread.start()
                ThreadCount += 1
                print('Thread Number: ' + str(ThreadCount))
            DB.close()
            ServerSocket.close()
        else:
            Client = ''
            player_id = 1
            print('Player ID: ' + str(player_id))
            print('SENT DATA: ' + str(self.trials_matrix))
            print()
            
            if player_id == 1:
                thread = DummyClientHandler(Client, DB, player_id, self.trials_matrix)
                response_vector = thread.Run(self.trials_matrix, indicator)
        return response_vector