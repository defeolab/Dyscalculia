import json
import random
import math
from AI.SimpleEvaluator import SimpleEvaluator
from AI.PDEP_Evaluator import PDEP_Evaluator

import time
from sys import exit
from json.decoder import JSONDecodeError
from threading import Thread
from server_utils.trial_result import TrialResult
from server_utils.trial_util import convert_trials_to_json, convert_matrix_to_trials
from server_utils.transform_matrix import TransformMatrix
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
    def __init__(self, lookup_table, client, db, player_id, evaluator, kids_ds, difficulty):
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
            self.player_evaluator = SimpleEvaluator(lookup_table, player_id, self.history_size, kids_ds=kids_ds)
        else:
            if difficulty == "regular":
                init_alpha = 45
                init_sigma = 0.3
            elif difficulty == "easy":
                init_alpha = 65
                init_sigma = 0.5
            self.player_evaluator = PDEP_Evaluator(init_alpha, init_sigma, norm_feats=True, mock=False, kids_ds=kids_ds, difficulty=difficulty)

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

            print("Diff: " + str(self.player_evaluator.get_stats(0)))
            
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
