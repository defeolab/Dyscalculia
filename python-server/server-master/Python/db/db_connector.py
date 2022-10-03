from typing import Any, Dict
from click import launch
import mysql.connector
from datetime import datetime
from trial import Trial
from area_data import AreaData
from trial_result import TrialResult

class DBConnector:

    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='12342234',
                                      host='127.0.0.1',
                                      database='dyscalculia')

    def add_player(self, username):
        cursor = self.cnx.cursor()
        add_player = ("INSERT INTO player (username) VALUES ('{}')".format(username))

        cursor.execute(add_player)

        self.cnx.commit()

        cursor.close()

        return cursor.lastrowid


    def add_player(self, address):
        cursor = self.cnx.cursor()

        # add player to the database
        add_player = ("INSERT INTO player (ip_address) VALUES (INET_ATON('{}'))".format(address))
        cursor.execute(add_player)

        self.cnx.commit()
        cursor.close()

        self.init_player_stats(cursor.lastrowid)

        return cursor.lastrowid

    def get_player(self, address):
        cursor = self.cnx.cursor()
        add_player = ("SELECT player_id FROM player WHERE ip_address = INET_ATON('{}') ".format(address))

        cursor.execute(add_player)

        results = list()
        for (player_id) in cursor:
            results.append(player_id)
        cursor.close()

        if len(results) > 1:
            print("More than one player_id for the specified ip address")
        elif len(results) < 1:
            print("No player found")
            return -1
        print("Recovered Player ID to: " + str(results[0][0]))
        return int(results[0][0])

    def add_player_stats(self, player, stats) :
        cursor = self.cnx.cursor()
        add_stats = (
            "INSERT INTO player_stats (sharp_total, filt_total, sharp_corr, filt_corr, sharp_acc, filt_acc, sharp_total_time, filt_total_time, sharp_avg_time, filt_avg_time, sharp_diff, filt_diff, player_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        data = (stats["sharpening_total"], stats["filtering_total"], stats["sharpening_correct"], stats["filtering_correct"],
            stats["sharpening_acc"], stats["filtering_acc"], stats["sharpening_total_time"], stats["filtering_total_time"], 
            stats["sharpening_avg_time"], stats["filtering_avg_time"], stats["sharpening_diff"], stats["filtering_diff"], player
        )
    
        cursor.execute(add_stats, data)
        self.cnx.commit()
        cursor.close()

    def init_player_stats(self, player_id) :
        cursor = self.cnx.cursor()
        add_stats = (
            "INSERT INTO player_info (player_id,filtering_total, filtering_correct, filtering_diff, filtering_total_time,sharpening_total, sharpening_correct, sharpening_diff, sharpening_total_time) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        data = (player_id, 0, 0, 0.1, 0, 0, 0, 0.1, 0)

        try:
            cursor.execute(add_stats, data)
            self.cnx.commit()
            cursor.close()
        except:
            print("something went wrong during player creation, aborting")
            cursor.execute("DELETE FROM player WHERE player_id = '{}'".format(player_id))
            self.cnx.commit()
            cursor.close()
            raise

    def get_player_stats(self, player_id: int, hystory_size: int) -> Dict[str, Any] :
        cursor = self.cnx.cursor()
        get_stats = ("SELECT * FROM player_info WHERE player_id = '{}'".format(player_id))

        cursor.execute(get_stats)
        running_results = {}

        for line in cursor:
            running_results["filtering_total"] = line[1] # total number of filtering trials
            running_results["filtering_correct"] = line[2]
            running_results["filtering_acc"] = -1 if line[1] <= 0 else line[2]/line[1]
            running_results["filtering_diff"] = float(line[3])
            running_results["filtering_total_time"] = line[4] # average time of responding to a filtering trial
            running_results["filtering_avg_time"] = -1 if line[4] <= 0 else line[4]/line[1]# average time of responding to a filtering trial
            running_results["filtering_history"] = []

            running_results["sharpening_total"] = line[5] # total number of sharpening trials
            running_results["sharpening_correct"] = line[6]
            running_results["sharpening_acc"] = -1 if line[5] <= 0 else line[6]/line[7]
            running_results["sharpening_diff"] = float(line[7])
            running_results["sharpening_total_time"] = line[8] # average time of responding to a sharpening trial
            running_results["sharpening_avg_time"] = -1 if line[8] <=0 else line[8]/line[5] # average time of responding to a sharpening trial
            running_results["sharpening_history"] = []
        
        cursor.close()

        return running_results


    def update_player_stats(self, player_id, new_stats) :
        pass

    def add_result(self, player_id, result):
        cursor = self.cnx.cursor()
        now = datetime.now()
        add_result = ("INSERT INTO trial_result_new (player_id, difficulty, trial_mode, correct, decision_time, "
                      "area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, "
                      "area_1_number_of_chickens, area_2_circle_radius, area_2_size_of_chicken, "
                      "area_2_average_space_between, area_2_number_of_chickens, chicken_show_time, created) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        result_trial_data = result.trial_data
        
        area_1_data = result_trial_data.area1Data
        area_2_data = result_trial_data.area2Data
        
        data_result = (player_id, result.difficulty, result.mode, result.correct, result.decision_time, area_1_data.circleRadius, 
                       area_1_data.sizeOfChicken, area_1_data.averageSpaceBetween, 
                       area_1_data.numberOfChickens, area_2_data.circleRadius, 
                       area_2_data.sizeOfChicken, area_2_data.averageSpaceBetween, 
                       area_2_data.numberOfChickens, 
                       result_trial_data.chickenShowTime, now)
        
        print(data_result)

        cursor.execute(add_result, data_result)

        self.cnx.commit()

        cursor.close()

    def add_results(self, player_id, results):
        for result in results:
            self.add_result(player_id, result)

    def get_results(self, player_id):
        cursor = self.cnx.cursor()

        query = ("SELECT trial_result_id, correct, decision_time, area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, area_1_number_of_chickens, area_2_circle_radius, area_2_size_of_chicken, area_2_average_space_between, area_2_number_of_chickens, chicken_show_time FROM trial_result_new "
                 "WHERE player_id = {}".format(player_id))

        cursor.execute(query)

        results = list()
        for (trial_result_id, correct, decision_time, area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, area_1_number_of_chickens, area_2_circle_radius, area_2_size_of_chicken, area_2_average_space_between, area_2_number_of_chickens, ratio, chicken_show_time) in cursor:
            # print("{}, {}, {}, {}, {}, {}, {}, {}".format(
            #     trial_result_id, correct, decision_time, area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, ratio, chicken_show_time))
            area_1_data = AreaData(area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, area_1_number_of_chickens)
            area_2_data = AreaData(area_2_circle_radius, area_2_size_of_chicken, area_2_average_space_between, area_2_number_of_chickens)
            trial_data = Trial(area_1_data=area_1_data, area_2_data=area_2_data, chicken_show_time=chicken_show_time, ratio=ratio)
            result = TrialResult(decision_time=decision_time, correct=correct, trial_data=trial_data)
            results.append(result)

        cursor.close()
        return results

    def close(self):
        self.cnx.close()

class DBException(BaseException):
    pass