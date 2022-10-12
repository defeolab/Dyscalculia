import socket
import pandas
from client_handler import ClientHandler, PlayerHandler
from dummy_client_handler import DummyClientHandler
 

class GameServer:

    def __init__(self, server_socket, host, port, db) -> None:
        self.server_socket = server_socket
        self.host = host 
        self.port = port
        self.db = db
        self.players = []
        self.running = True
        
        # lookup table is shared in the server to avoid multiple opens
        self.lookup_table = pandas.read_csv("./dataset/lookup_table.csv")

    def run(self):

        try :
            self.server_socket.bind((self.host, self.port))
        except socket.error as e :
            print(str(e))
        
        print('Waiting for a Connection..')
        self.server_socket.listen(5)
        
        while self.running :
            # Accepting player connection
            client, address = self.server_socket.accept()
            player_id = self.db.get_player(address[0])
            if player_id == - 1:
                player_id = self.db.add_player(address[0])
            print("Player " + str(player_id) + " has joined")

            # Starting a thread to handle the player
            player_thread = PlayerHandler(self.lookup_table, client, self.db, player_id)
            player_thread.run()
            self.players.append(player_thread)
            print("Number of players: " + str(len(self.players)))
            



# LEGACY
class Create_Game:
    
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
           
    def run(self, simulation_on, nnd_selector, alpha, sigma, ServerSocket, host, port, DB, ThreadCount):
        
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
                # performing the ChildSimulator method, which represents the simulation of a child
                # playing our game, and obtain back a response_vector, in its simulated version
                response_vector = game.Run(self.trials_matrix, nnd_selector, alpha, sigma)
        return response_vector