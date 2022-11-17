import json
import random
import math
from AI.SimpleEvaluator import SimpleEvaluator
from AI.PDEP_Evaluator import PDEP_Evaluator
import settings_manager

import time
from sys import exit
from json.decoder import JSONDecodeError
from threading import Thread
from trial import Trial
from trial_result import TrialResult
from correlated_data_generator import generate_correlated_trials
from trial_util import convert_trials_to_json, convert_matrix_to_trials
from transform_matrix import TransformMatrix
from trial_mode_utils import qserver_ask_for_question_recommendation
import random
import socket

def calculate_next_correlation(average_decision_time, correct_answer_ratio):
    if correct_answer_ratio < 0.3:
        return 1.00
    elif correct_answer_ratio < 0.5:
        if average_decision_time < 1000:
            return 0.30
        elif average_decision_time < 2000:
            return 0.50
        elif average_decision_time < 3000:
            return 0.7
        elif average_decision_time < 4000:
            return 1.0
    elif correct_answer_ratio < 0.7:
        if average_decision_time < 1000:
            return 0.10
        elif average_decision_time < 2000:
            return 0.30
        elif average_decision_time < 3000:
            return 0.50
        elif average_decision_time < 4000:
            return 0.70
    elif correct_answer_ratio < 0.9:
        if average_decision_time < 1000:
            return 0.05
        elif average_decision_time < 2000:
            return 0.20
        elif average_decision_time < 3000:
            return 0.30
        elif average_decision_time < 4000:
            return 0.40
    else:
        return 0.00

class PlayerHandler(Thread) :
    def __init__(self, lookup_table, client, db, player_id, evaluator):
        super().__init__()
        self.client = client 
        self.db = db
        self.player_id = player_id
        self.running = True
        self.lookup_table = lookup_table
        self.first_communication = True # sending trials is different for the first run, should probably be changed
        self.mode = "filtering" # 0 for sharpening | 1 for filtering
        self.num_trials = 1 # number of trials sent to the client at a time
        self.history_size = 5 

        self.evaluator_type = evaluator
        if evaluator == "simple":
            self.player_evaluator = SimpleEvaluator(lookup_table, player_id, self.history_size)
        else:
            init_alpha = 45
            init_sigma = 0.2
            self.player_evaluator = PDEP_Evaluator(init_alpha, init_sigma, norm_feats=True, mock=False)

    def run(self) :

        #At this point there must be data about this player's statistics
        #load them and run the player

        #fetch stats from db
        self.player_evaluator.db_set_running_results(self.db, self.player_id)

        #assert True == False
        print("Game " + str(self.player_id) + " is running") 
        while self.running :
            try:
                data = self.client.recv(2048)
                reply = self.process_reply(data.decode("utf-8"))
                self.client.send(str.encode(reply))
            except socket.error as e :
                print(e)
                self.running = False
                break
        time.sleep(0.5)
        print("terminating thread")

    def process_reply(self, data) :
        if data.strip() == "TRIAL" :
            pass
        elif "TRIALS:" in data :
            print("SENDING TRIALS TO GAME")

            print("Diff: " + str(self.player_evaluator.get_stats()))
            
            trials_matrix = TransformMatrix(self.player_evaluator.get_trial())
            return convert_trials_to_json(convert_matrix_to_trials(trials_matrix))
   

        elif "COMPLETE:" in data:
            # Process results json
            print("PROCESSING TRIALS RESULTS")
            # TODO WHY DOES IT SEND THE ENTIRE THING IN TWO PACKAGES? WHY NOT A SINGLE ONE?
            data = data[9:]
            # print(data)
            # print("###################################")
            data = data.strip()
            while data[-2:] != "]}" :
                new_data = self.client.recv(2048).decode("utf-8").strip()
                data += new_data
            
            #print(data)

            # Update database for the player and update running results
            
            print("ADDING RESULTS TO DATABASE")
            try:
                results = json.loads(data)
            except JSONDecodeError:
                return "Failed to decode\n"

            results_to_add = []
            correct = 0
            for result in results["results"] :
                results_to_add.append(TrialResult(mode = self.player_evaluator.mode, difficulty = self.player_evaluator.get_main_stat(), decision_time=result["DecisionTime"], correct=result["Correct"], raw_trial_data=result["TrialData"]))
                correct += int(result["Correct"])

            # updating player stats
            self.player_evaluator.update_statistics(correct, result["DecisionTime"])
            #print(self.running_results[self.mode + "_history"])

            # update player stats in the database
            #print(self.player_evaluator.running_results)
            self.player_evaluator.db_update(self.db, self.player_id, results_to_add)

            return "SUCCESS" + "\n"

        elif "SETTINGS:" in data:
            pass
        elif "END:" in data:
            self.running = False
        
        return "SERVER SAYS: " + data
    
    #moved to player_evaluate
    def lookup_trials(self) :
        margin = 0.005

        total_trials = self.num_trials

        if self.mode == "filtering" :
            col = "Diff_coeff_filtering"
        else :
            col = "Difficulty Coefficient"

        target_diff = self.running_results[self.mode + "_diff"]

        trial = self.lookup_table.iloc[(self.lookup_table[col]-target_diff).abs().argsort()[:2]]

        # alternating sides
        if random.uniform(0, 1) >= 0.5 :
            r = trial.iloc[0]
        else :
            r = trial.iloc[1]

        # generate trial matrices
        matrix = []
        matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]), 4, 8])
        print("NUMBER OF TRIALS SENT: " + str(len(matrix)))
        return matrix

# Legacy
class ClientHandler(Thread):

    def __init__(self, connection, db, player_id, trials_matrix):
        super().__init__()
        self.connection = connection
        self.db = db
        self.player_id = player_id
        self.settings = settings_manager.load_from_xml()
        self.results = list()
        self.trials_matrix = trials_matrix

    def run(self):
        print("1 RUN FUNCTION")
        while True:
            data = self.connection.recv(2048) 
            reply = self.get_reply(data.decode('utf-8'))
            if not data:
                break
            self.connection.send(str.encode(reply))
            print('Sent: ' + reply)
        print('Connection Closed')
        self.connection.close()

    def get_reply(self, data):
        print("2 GET REPLY")
        # Must terminate reply with \n
        if data.strip() == 'TRIAL':
            print("ENTRATA NEL POSTO RANDOM")
            trial = self.generate_random_trial()
            return json.dumps(trial.__dict__) + '\n'
        elif "TRIALS:" in data:
            return self.handle_trials_message(data.split(":")) # when we receive smth from client
        elif "COMPLETE:" in data:
            print("Those are the complete trials received by the client")
            print(data)
            return self.handle_complete_message(data[9:].strip())
        elif "SETTINGS:" in data:
            return self.handle_settings_message(data[9:])
        return 'Server Says: ' + data
    
    def PlayGame (self, trials_matrix):
        return convert_matrix_to_trials(self.trials_matrix) 
     
    def handle_trials_message(self,data):
        print("3 handle_trials_message FUNCTION")
        number_of_trials = int(data[1])
        if len(self.results) == 0:
             print("GENERATING UNCORRELATED TRIALS")
             trials = self.PlayGame(number_of_trials)
             #return PlayGame(number_of_trials)
        else:
            print("GAME ENDED")
            exit()
            #print("GENERATING CORRELATED TRIALS")
            #trials = self.generate_trials_from_results(number_of_trials)
        return convert_trials_to_json(trials)
        
    
    def handle_complete_message(self, data):
        print("4 handle_complete_message FUNCTION")
        while data[-1] != "}":
            old_string = data
            new_data = self.connection.recv(2048)     
            data = new_data.decode('utf-8')
            data = old_string + data.strip()
        try:
            result = json.loads(data)
        except JSONDecodeError:
            return "Failed to decode\n"
        self.add_results(result['results'])
        return "SUCCESS" + '\n'

    def handle_settings_message(self, data):
        print("5 handle_settings_message FUNCTION")
        result = json.loads(data)
        self.save_settings(result)
        return "SUCCESS" + '\n'

    def add_results(self, results):
        print("6 add_results FUNCTION")
        self.results = []
        for result in results:
            self.results.append(TrialResult(decision_time=result['DecisionTime'], correct=result['Correct'], raw_trial_data=result['TrialData']))
        self.db.add_results(self.player_id, self.results)
        print("THIS IS THE RESULT ARRAY")
        print(results)
        response_vector = [result.get_answer() for result in self.results]
        print("THIS IS THE RESPONSE VECTOR")
        print (response_vector)

    def save_settings(self, settings):
        print("7 save_settings FUNCTION")
        self.settings.ratio_min = settings["RatioMin"]
        self.settings.ratio_max = settings["RatioMax"]
        self.settings.average_space_between_min = settings["AverageSpaceBetweenMin"]
        self.settings.average_space_between_max = settings["AverageSpaceBetweenMax"]
        self.settings.size_of_chicken_min = settings["SizeOfChickenMin"]
        self.settings.size_of_chicken_max = settings["SizeOfChickenMax"]
        self.settings.total_area_occupied_min = settings["TotalAreaOccupiedMin"]
        self.settings.total_area_occupied_max = settings["TotalAreaOccupiedMax"]
        settings_manager.save_to_xml(self.settings)

    def generate_random_trial(self):
        print("8 generate_random_trial FUNCTION")
        """
        Generates a completely random trial based on settings values. Parameters are:

        ratio: Ratio to apply to multiply all the variables by on one side
        average_space_between: Average space between the chickens
        size_of_chicken: Size of the chicken
        total_area_occupied: Total area occupied by the chickens
        chicken_show_time: Total time the chickens appear on screen for before disappearing to avoid people just counting the chickens
        max_trial_time: Maximum time the trial can last before automatically being moved on as incorrect
        number_of_chickens: Number of chickens in the circle

        :return: Trial object with all parameters stored in
        """
        average_space_between = random.uniform(self.settings.average_space_between_min,
                                               self.settings.average_space_between_max)
        size_of_chicken = random.uniform(self.settings.size_of_chicken_min, self.settings.size_of_chicken_max)
        total_area_occupied = random.uniform(self.settings.total_area_occupied_min,
                                             self.settings.total_area_occupied_max)
        circle_radius = math.sqrt(total_area_occupied / math.pi)
        chicken_show_time = random.uniform(self.settings.chicken_show_time_min, self.settings.chicken_show_time_max)
        max_trial_time = random.uniform(self.settings.max_trial_time_min, self.settings.max_trial_time_max)
        number_of_chickens = random.randint(2, 8)
        return Trial(None, None, circle_radius, circle_radius, size_of_chicken,
                     size_of_chicken, average_space_between, average_space_between,
                     number_of_chickens, number_of_chickens,
                     chicken_show_time, max_trial_time)

   

    def generate_trials_from_results(self, number_of_trials):
        print("9 generate_trials_from_results FUNCTION")
        """
        Generates the next set of trials based on the persons results so far currently this is done by using a very
        simple AI with conditional statements to pick the next correlation and then generate a set of trials based
        on this correlation.

        There is the matrix version of the trial played currently commented out as well as the array of results,
        these can be used to create a more sophisticated AI all this method needs to do is return a list of trials.

        trials_matrix takes the format of [[ratio, average_space_between, size_of_chicken, circle_radius (for total_area_occupied), chicken_show_time, max_trial_time, ratio_area],
                                           [...],
                                           [...]]
        the number of rows will equal the number of trials in the results variable.

        The ratio area variable is the area which the ratio was applied to 0 for right side and 1 for left side

        results area is a array filled with either 0 or 1 for each trial 0 means the selected area by the player was
        incorrect and 1 means it was correct

        :return: array of Trial objects
        """
       
        self.settings = settings_manager.load_from_xml()
        next_correlation = self.get_next_correlation()
        if next_correlation == 0:
            print("Next Correlation 0 generating uncorrelated trials")
            return self.generate_trials(number_of_trials)
        return generate_correlated_trials(number_of_trials, next_correlation, self.settings)

    def get_next_correlation(self):
        print("10 get_next_correlation FUNCTION")
        total_decision_time = 0
        number_of_correct_answers = 0
        for result in self.results:
            total_decision_time += result.decision_time
            if result.correct:
                number_of_correct_answers += 1
        average_decision_time = total_decision_time / len(self.results)
        correct_answer_ratio = number_of_correct_answers / len(self.results)
        next_correlation = calculate_next_correlation(average_decision_time, correct_answer_ratio)
        return next_correlation