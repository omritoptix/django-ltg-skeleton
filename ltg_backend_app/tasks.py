'''
will hold our app tasks
Created on May 12, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''
#===============================================================================
# begin imports
#===============================================================================

from __future__ import absolute_import
from ltg_backend_app.celery import app
from ltg_backend_app.models import Attempt, MAX_ALGORITHM_ATTEMPTS,\
    QuestionStatistics, Question, MIN_ATTEMPT_DURATION
from ltg_backend_app.tasks_helpers import calc_time_statistics,\
    calc_percentage_right_and_score, calc_percentage_wrong

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin tasks
#===============================================================================
 
@app.task
def update_questions_statistics():
    '''
    update all questions statistics paramaters:
    mean_time, std_time, percentage_right, percentage_wrong, score.
    '''
    # get all the questions
    question_qs = Question.objects.all()
    # iterate over all questions and update the statistics
    for question in question_qs:
        # init params
        attempt_num = 1
        is_attempt_valid = True
        # query set to hold all the attempts for the current question (query set not evaluated yet)
        question_attempt_qs = Attempt.objects.filter(question_id = question.id)
        # loop while there is an attempt for the question or attempt num is up to 5
        while (is_attempt_valid and attempt_num <= MAX_ALGORITHM_ATTEMPTS):
            # if attempt exists for the question, iterate over all attempts for the question and calc the time statistics
            if question_attempt_qs.filter(attempt = attempt_num).exists():
                # update the question attempt query set with the current attempt and filter upon duration time
                question_specific_attempt_qs = question_attempt_qs.filter(attempt = attempt_num,duration__gt = MIN_ATTEMPT_DURATION) 
                # get time statistics 
                mean_time,std_time = calc_time_statistics(question_specific_attempt_qs, question)
                # get percentage right
                percentage_right, score = calc_percentage_right_and_score(question_specific_attempt_qs,question)           
                # save to question statistics
                try:
                    # incase there is such object already, update it
                    question_statistics = QuestionStatistics.objects.get(question_id = question.id, attempt = attempt_num)
                    # calc the percentage wrong and update the relevant question
                    calc_percentage_wrong(question_specific_attempt_qs,question,question_statistics)
                    question_statistics.mean_time = mean_time
                    question_statistics.std_time = std_time
                    question_statistics.percentage_right = percentage_right
                    question_statistics.score = score
                    question_statistics.save()
                    
                except QuestionStatistics.DoesNotExist:
                    # if there isn't an object, create it.
                    question_statistics = QuestionStatistics.objects.create(question_id = question.id, attempt = attempt_num, mean_time = mean_time, std_time = std_time, percentage_right = percentage_right, score = score)
                    # calc the percentage wrong and update the relevant question
                    calc_percentage_wrong(question_specific_attempt_qs,question,question_statistics)
                    
                # update attempt number            
                attempt_num += 1
            else:
                is_attempt_valid = False
                

#===============================================================================
# end tasks
#===============================================================================