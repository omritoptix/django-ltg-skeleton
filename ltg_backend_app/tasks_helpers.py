'''
will hold our tasks helpers methods
Created on May 13, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

import numpy
from ltg_backend_app.models import ScoreTable, ANSWER, WrongAnswersPercentage
from ltg_backend_app.api.hubspot_client import HubSpotClient
from ltg_backend_app import settings

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin update_question_statistics task helpers
#===============================================================================

def calc_time_statistics(question_attempt_qs,question):
    '''
    will calculate time statistics for the given Attempt query set and a question
    @param QuerySet question_attempt_qs : a query set of type attempt for a specific question
    @param Model question : a Question model object to calc the statistics for
    @return: mean time and std time for the question
    '''
    # will hold the times for each attempt
    durations_per_attempt = []
    for duration_per_attempt in question_attempt_qs.values_list('duration',flat=True):
        durations_per_attempt.append(duration_per_attempt.total_seconds())
      
    # calc time statistics per attempt 
    mean_time = int(numpy.mean(durations_per_attempt))
    std_time = int(numpy.std(durations_per_attempt))
    
    return mean_time,std_time
                        

def calc_percentage_right_and_score(question_attempt_qs,question):
    '''
    calc the percetage of people who answered this question right and the score for a given question
    @param QuerySet question_attempt_qs : a query set of type attempt for a specific question
    @param Model question : a Question model object to calc the statistics for
    @return: percentage  right and score for the question
    '''   
    # calc percentage right
    total_answers = question_attempt_qs.count()
    right_answers = question_attempt_qs.filter(answer = question.answer).count()
    percentage_right =  ((float(right_answers)/total_answers) * 100)
    
    # calc score
    percentile = 100 - percentage_right
    # get percentile and score edges for the interpolation
    percentile_ceil = ScoreTable.objects.filter(percentile__gte = percentile).first().percentile
    percentile_floor = ScoreTable.objects.filter(percentile__lte = percentile).last().percentile
    score_ceil = ScoreTable.objects.get(percentile = percentile_ceil).score
    score_floor = ScoreTable.objects.get(percentile = percentile_floor).score
    # allocate new lists to hold the x,y coordinates (i.e percentile and score coordinates)
    percentile_data_points, score_data_points = [],[]
    percentile_data_points.extend([percentile_floor,percentile_ceil])
    score_data_points.extend([score_floor,score_ceil])
    # calc score based on linear interpolation
    question_score = numpy.interp(percentile, percentile_data_points, score_data_points)
    # round the score 
    score =  int(round(question_score))

    return percentage_right,score


def calc_percentage_wrong(question_attempt_qs,question,question_statistics):
    '''
    calc the ditrubution in percentage for each wrong answer.
    update/create the WrongAnswerPercentage model with the result
    @param QuerySet question_attempt_qs : a query set of type attempt for a specific question
    @param Model question : a Question model object to calc the statistics for
    @param Model question_statistics : a QuestionStatistics model object to be used as a fk in the WrongAnswerPercentage model
    '''   
    total_wrong_answers = question_attempt_qs.exclude(answer = question.answer).count()
    # populate wrong answers list
    wrong_answers = []
    for answer in ANSWER:
        if answer[0] != question.answer:
            wrong_answers.append(answer[0])
    # if there are no wrong answer for the question ,update wrong answer question object with 0 percentage for each wrong answer 
    if (total_wrong_answers == 0):
        for wrong_answer in wrong_answers:
            try:
                wrong_answers_percentage = WrongAnswersPercentage.objects.get(question_statistics_id = question_statistics.id, answer = wrong_answer)
                wrong_answers_percentage.percentage_wrong = 0
                wrong_answers_percentage.save()
            except WrongAnswersPercentage.DoesNotExist:
                WrongAnswersPercentage.objects.create(question_statistics_id = question_statistics.id, answer = wrong_answer, percentage_wrong = 0)
    # if there are wrong answers - calc percentage distribution of each one
    else:
        # calc wrong answers percentage and update WrongAnswerPercentage model accordingly
        for wrong_answer in wrong_answers:
            num_wrong_answers = question_attempt_qs.filter(answer = wrong_answer).count()
            percentage_wrong = (float(num_wrong_answers)/total_wrong_answers) * 100
            try:
                wrong_answers_percentage = WrongAnswersPercentage.objects.get(question_statistics_id = question_statistics.id, answer = wrong_answer)
                wrong_answers_percentage.percentage_wrong = percentage_wrong
                wrong_answers_percentage.save()
            except WrongAnswersPercentage.DoesNotExist:
                wrong_answers_percentage = WrongAnswersPercentage.objects.create(question_statistics_id = question_statistics.id, answer = wrong_answer, percentage_wrong = percentage_wrong)
                
                
#===============================================================================
# end update_question_statistics task helpers
#===============================================================================

#===============================================================================
# hubspot task helpers
#===============================================================================

def hubspot_client():
        #define our api client
        return HubSpotClient(settings.HUBSPOT_API_KEY)
    
#===============================================================================
# end hubspot task helpers
#===============================================================================