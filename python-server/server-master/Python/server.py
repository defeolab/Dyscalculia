import socket
from client_handler import ClientHandler
from dummy_client_handler import DummyClientHandler
 
class Create_Game:
    
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
           
    def run(self, simulation_on, nnd_selector, alpha, ServerSocket, host, port, DB, ThreadCount):
        
        # REAL GAME
        if simulation_on == 0:
            try:
                # bind() method assigns an IP address and a port number 
                # to a socket instance. So, in a way, it binds the port number
                # with the IP address
                ServerSocket.bind((host, port))
            except socket.error as e:
                print(str(e))
            
            print('Waiting for a Connection..')
            # In order to accept a connection, the server must stay in a 
            # 'listening' position
            ServerSocket.listen(5)
            
            while True:
                # When the client wants to establish the connection, the server 
                # must accept it --> method .accept(), which returns:
                    # Client: is a new socket object usable to send and receive 
                    # data on the connection 
                    # Address: is the address bound to the socket on the other 
                    # end of the connection.
                Client, address = ServerSocket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                player_id = DB.get_player(address[0])
                if player_id == - 1:
                    player_id = DB.add_player(address[0])
                # gameThread becomes an Object of class ClientHandler, which
                # is a thread, so to make it actually running, we must call the
                # start() method on it, which calls automatically the run() method
                gameThread = ClientHandler(Client, DB, player_id, self.trials_matrix)
                response_vector = gameThread.start()
                ThreadCount += 1
                print('Thread Number: ' + str(ThreadCount))
            # Once all is done, close the DB instance and the Socket one
            DB.close()
            ServerSocket.close()
        # SIMULATED GAME
        else:
            Client = ''
            player_id = 1
            print('Player ID: ' + str(player_id))
            print('SENT DATA: ' + str(self.trials_matrix))
            print()
            
            if player_id == 1:
                # Instantiate an Object of class DummyClientHandler, whose method
                # init requires the trials_matrix only to be initialized, so
                # this is why we only pass the trials_matrix and nothing else.
               
                game = DummyClientHandler(self.trials_matrix)
                
                # Calling the Run() method, we actually run the simulated game,
                # performing the Analysis and obtain back a response_vector, it is
                # simulated version
                response_vector = game.Run(self.trials_matrix, nnd_selector, alpha)
        return response_vector