import json
import random
import math
import settings_manager

from sys import exit
from json.decoder import JSONDecodeError
from threading import Thread
from trial import Trial
from trial_result import TrialResult
from correlated_data_generator import generate_correlated_trials
from trial_util import convert_trials_to_json, convert_matrix_to_trials


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
        while True:
            data = self.connection.recv(2048)
            reply = self.get_reply(data.decode('utf-8'))
            if not data:
                break
            self.connection.send(str.encode(reply))
            print('Sent ' + reply)
        print('Connection Closed')
        self.connection.close()

    def get_reply(self, data):
        # Must terminate reply with \n
        if data.strip() == 'TRIAL':
            trial = self.generate_random_trial()
            return json.dumps(trial.__dict__) + '\n'
        elif "TRIALS:" in data:
            return self.handle_trials_message(data.split(":"))
        elif "COMPLETE:" in data:
            return self.handle_complete_message(data[9:].strip())
        elif "SETTINGS:" in data:
            return self.handle_settings_message(data[9:])
        return 'Server Says: ' + data
    
    def PlayGame (self, trials_matrix):
        return convert_matrix_to_trials(self.trials_matrix) 
     
    def handle_trials_message(self,data):
        number_of_trials = int(data[1])
        if len(self.results) == 0:
             print("GENERATING UNCORRELATED TRIALS")
             trials = self.PlayGame(number_of_trials)
             #return PlayGame(number_of_trials)
        else:
            print("GAME ENDED")
            exit()
        return convert_trials_to_json(trials)
        
    
    def handle_complete_message(self, data):
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
        result = json.loads(data)
        self.save_settings(result)
        return "SUCCESS" + '\n'

    def add_results(self, results):
        self.results = []
        for result in results:
            self.results.append(TrialResult(decision_time=result['DecisionTime'], correct=result['Correct'], raw_trial_data=result['TrialData']))
        self.db.add_results(self.player_id, self.results)
        print(results)
        response_vector = [result.get_answer() for result in self.results]
        return response_vector

    def save_settings(self, settings):
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
        ratio = random.uniform(self.settings.ratio_min, self.settings.ratio_max)
        average_space_between = random.uniform(self.settings.average_space_between_min,
                                               self.settings.average_space_between_max)
        size_of_chicken = random.uniform(self.settings.size_of_chicken_min, self.settings.size_of_chicken_max)
        total_area_occupied = random.uniform(self.settings.total_area_occupied_min,
                                             self.settings.total_area_occupied_max)
        circle_radius = math.sqrt(total_area_occupied / math.pi)
        chicken_show_time = random.uniform(self.settings.chicken_show_time_min, self.settings.chicken_show_time_max)
        max_trial_time = random.uniform(self.settings.max_trial_time_min, self.settings.max_trial_time_max)
        number_of_chickens = random.randint(2, 8)
        return Trial(None, None, circle_radius, size_of_chicken, average_space_between, ratio, chicken_show_time, max_trial_time, number_of_chickens)

   

    def generate_trials_from_results(self, number_of_trials):
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