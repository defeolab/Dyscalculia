import socket
import random
import math
from client_handler import ClientHandler
from dummy_client_handler import DummyClientHandler
 
class Flag(): 
    #create the random matrix for the real game 
    def generate_random_trial_matrix(self):
        n = round(random.uniform(1, 10)) #gives a random length for the rows of the matrix
        trials_matrix = []
        for i in range (n):
            ratio = round (random.uniform(0,2), 1)
            average_space_between = round (random.uniform(1,2), 1)
            size_of_chicken = round (random.uniform(0.5,2), 1)
            total_area_occupied = round (random.uniform(2,3))
            circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
            chicken_show_time = round (random.uniform(2,5))
            max_trial_time = round (random.uniform(8,10))
            ratio_area = round (random.randint(0, 1))
            
            trials_list = []
            
            trials_list.append(ratio)
            trials_list.append(average_space_between)
            trials_list.append(size_of_chicken)
            trials_list.append(circle_radius)
            trials_list.append(chicken_show_time)
            trials_list.append(max_trial_time)
            trials_list.append(ratio_area)
             
            trials_matrix.append(trials_list)
        #print(np.shape(trials_matrix))
        return trials_matrix
    
    #create the matrix for the dummy game 
    def generate_dummy_random_trial_matrix(self):
        n = round(random.uniform(1, 100)) #gives a random length for the rows of the matrix
        trials_matrix = []
        for i in range (n):
            ratio = round (random.uniform(1.1,2), 1)
            average_space_between = round (random.uniform(1,2), 1)
            size_of_chicken = (random.uniform(0.1,2))
            total_area_occupied = round (random.uniform(2,3))
            circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
            number_of_chickens = random.randint(8, 15)
            number_of_chickens2 = round (int(number_of_chickens * ratio))
        
            trials_list1 = []
            
            trials_list1.append(circle_radius)
            trials_list1.append(size_of_chicken)
            trials_list1.append(average_space_between)
            
            trials_list2 = [i * ratio for i in trials_list1]
            trials_list1.append(number_of_chickens)
            trials_list1.extend(trials_list2)
            trials_list1.append(number_of_chickens2)
            trials_list1.append(ratio)
     
            trials_matrix.append(trials_list1)
        #print(np.shape(trials_matrix))
        return trials_matrix
           
    def run(self, flag, ServerSocket, host, port, DB, ThreadCount):
        if flag == 1:
            try:
                ServerSocket.bind((host, port))
            except socket.error as e:
                print(str(e))
            
            print('Waiting for a Connection..')
            ServerSocket.listen(5)
            
            while True:
                trials_matrix = self.generate_random_trial_matrix();
                Client, address = ServerSocket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                player_id = DB.get_player(address[0])
                if player_id == - 1:
                    player_id = DB.add_player(address[0])
                thread = ClientHandler(Client, DB, player_id, trials_matrix)
                thread.start()
                ThreadCount += 1
                print('Thread Number: ' + str(ThreadCount))
            DB.close()
            ServerSocket.close()
        else:
            trials_matrix = self.generate_dummy_random_trial_matrix();
            print('Connected to: ' + host)
            Client = ''
            player_id = 1
            print('Player ID: ' + str(player_id))
            print('SENT DATA: ' + str(trials_matrix))
            print()
            
            if player_id == 1:
                thread = DummyClientHandler(Client, DB, player_id,trials_matrix)
                thread.Run(trials_matrix) 
            
