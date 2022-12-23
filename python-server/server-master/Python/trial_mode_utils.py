import random

def qserver_return_other_question_type(question_type):
    if question_type.lower == 'f':
        return 's'
    else:
        return 'f'
    

def qserver_suggest_next_question (current_question_type, current_question_score , 
                                   all_question_and_Score, last_x_trial_to_consider):
    last_question_asked=''
    last_score_given =0
    last_no_of_questions_to_use =0
    accuracy_for_s_question = 0
    accuracy_for_f_question = 0
    
#     print(all_questions)
#     print(all_scores)

#    Check if this is the first call.
    if len(all_question_and_Score) == 0:
        # print
        other_question_type = qserver_return_other_question_type(current_question_type)
        return other_question_type
    
        # s,f
    if last_x_trial_to_consider > len(all_question_and_Score):
        last_no_of_questions_to_use = len(all_question_and_Score)
    else:
        last_no_of_questions_to_use = last_x_trial_to_consider
    


    #Loop through and get the Accuracy based on number of questions to use
    # Set of last questions to consider... new_all_question_and_Score ********
    new_all_question_and_score_to_consider = all_question_and_Score[-last_no_of_questions_to_use:]
    
    #Now Calclate Accuracy of S and F question by counting number of s and f questions in new_all_question_and_score_to_consider
    count_of_s_question =0
    count_of_f_question =0
    sum_of_s_scores =0
    sum_of_f_scores =0
    
    for x in new_all_question_and_score_to_consider:
         #Sample x Record ['f',3]
        if x[0] == 'f': 
            count_of_f_question +=1
            sum_of_f_scores += int(x[1])
        else:
            count_of_s_question +=1
            sum_of_s_scores += int(x[1])
    
    print('count_of_f_question:' + str(count_of_f_question))
    print('count_of_s_question:' + str(count_of_s_question))
    print('sum_of_f_question:' + str(sum_of_f_scores))
    print('sum_of_s_question:' + str(sum_of_s_scores))
    
    
    maximum_score_possible_f = count_of_f_question * 3 
    maximum_score_possible_s = count_of_s_question * 3 
    
    accuracy_of_f =0
    if maximum_score_possible_f !=0:
        accuracy_of_f = sum_of_f_scores/maximum_score_possible_f
    
    accuracy_of_s =0
    if maximum_score_possible_s !=0:
        accuracy_of_s = sum_of_s_scores/maximum_score_possible_s

    #print('accuracy_of_f:' + str(accuracy_of_f))
    #print('accuracy_of_s:' + str(accuracy_of_s))
    
    
    #Now check which question has the lowest accuracy and return it
    question_to_return =''
    
    if accuracy_of_s < accuracy_of_f:
        question_to_return = 's'
    elif accuracy_of_s > accuracy_of_f:
        question_to_return = 'f'
    else:
        #At this point let the system use random numbers
        random_list = ['f','s'] #This are the two possible question types
        random_question_from_List = random.choice(random_list)
        question_to_return = random_question_from_List
       
    

    
    return question_to_return 



# This is the function that will be called by the other code.
def qserver_ask_for_question_recommendation(question_type, 
                                            question_answer_status,
                                            time_taken_to_answer, 
                                            question_and_score_history,
                                            db_question_score = None):
  
    #Assign history coming from client   
    all_questions_and_scores =question_and_score_history

    last_x_trial_to_consider = 4 

# Calculte Question Score
# NOTE: question_answer_status is 1 when Answered correctly and 0 if wrong
    question_score =0
    max_limit_in_mseconds_to_get_3 = 5000
    max_limit_in_mseconds_to_get_2 = 20000
    

    if question_answer_status:
      # check how long it took.
      if time_taken_to_answer <= max_limit_in_mseconds_to_get_3:
        question_score = 3
      elif time_taken_to_answer > max_limit_in_mseconds_to_get_3 and time_taken_to_answer <= max_limit_in_mseconds_to_get_2:
        question_score = 2
      else:
        question_score = 1
    else:
      # Becos the candidate got it wrong i.e question_answer_status ==0
      
      question_score = 1
    
    if db_question_score is not None:
        #this value is used just as initialization of the mode at the very first trial
        question_score = db_question_score
    
    print('question_answer_status is : ' + str(question_answer_status))
    print('question_score is : ' + str(question_score))


    
#Create Question History e.g [["F",2],["S",1]]
    a_question_and_score = []
    a_question_and_score.append(question_type.lower())
    a_question_and_score.append(question_score)
    # a_question_and_score = ["F",2]
    
    all_questions_and_scores.append(a_question_and_score)
    # all_questions_and_scores = [["F",2],["S",1],["F",3]]

    
    #Time to get question suggestion:
    # Make a copy To preserve the original array becuase of array reference.
    all_questions_and_scores_copy = all_questions_and_scores.copy()     
    nextquestion = qserver_suggest_next_question(question_type, question_score ,
                                             all_questions_and_scores_copy,
                                             last_x_trial_to_consider)

#Create the return array for the calling client
    return_array_for_client = []
    return_array_for_client.append(nextquestion) #Add the next question
    return_array_for_client.append(all_questions_and_scores) # Add the History array
    
#   Sample return_array_for_client = ['f', [['f', '2'], ['s', '1'], ['s', '1'], ['s', '3'], ['s', '3']]]
#     print(return_array_for_client)
    return return_array_for_client
