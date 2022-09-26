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


    def get_player_stats(self, player_id) :
        pass

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