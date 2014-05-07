# -*- coding: utf-8 -*-
'''
contains the db models
Created on April 1st, 2014

@author: Yariv Katz & Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from django.db import models
import datetime
from django.contrib.auth.models import User
import logging
from tastypie.models import create_api_key
from django.utils.timezone import utc
from functools import wraps
from timedelta.fields import TimedeltaField
import numpy
from django.utils.functional import cached_property

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

ANSWER = (
    (0, 'A'),
    (1, 'B'),
    (2,  'C'),
    (3,  'D'),
    (4,  'E'),
)

# max attempts for a question to calc statistics for
MAX_ALGORITHM_ATTEMPTS = 5
# percentage right to return when no one answered this question yet
QUESTION_PERCENTAGE_NO_ANSWERS = 100.0

#===============================================================================
# end constants
#===============================================================================

#===============================================================================
# begin globals
#===============================================================================

logger = logging.getLogger()

#===============================================================================
# end globals
#===============================================================================

#===============================================================================
# begin models abstract classes
#===============================================================================

class LtgModel(models.Model):
    '''
    this class will be an abstract class for all my models
    and it will contain common information
    '''
    creation_date = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0,tzinfo=utc))
    modified_data = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0,tzinfo=utc), auto_now=True)
    
    class Meta:
        abstract = True
                
#===============================================================================
# end models abstract classes
#===============================================================================

#===============================================================================
# begin tables - models
#===============================================================================

class Concept(LtgModel):
    '''
    will hold the concept model
    '''
    title = models.CharField(unique=True,max_length=200)
    
    def __unicode__(self):
        return self.title
    
    def natural_key(self):
        return self.title
    
    @cached_property
    def statistics(self):
        concept_scores = UserConceptScore.objects.filter(concept_id = self.id).values_list('score')
        mean = numpy.mean(concept_scores)
        std = numpy.std(concept_scores)
        return {'mean':mean,'std':std}
    
class ConceptManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)
    
class Section(LtgModel):
    '''
    will hold the section model
    '''
    title = models.CharField(unique=True,max_length=200)
    
    def __unicode__(self):
        return self.title
    
    def natural_key(self):
        return self.title
    
    @cached_property
    def statistics(self):
        section_scores = UserSectionScore.objects.filter(section_id = self.id).values_list('score')
        mean = numpy.mean(section_scores)
        std = numpy.std(section_scores)
        return {'mean':mean,'std':std}
    
    
class UserProfile(LtgModel):
    '''
    will hold the user profile model
    '''
    user = models.ForeignKey(User, unique=True)
    uuid = models.CharField(max_length=200, default=None, unique=True)
    is_anonymous = models.BooleanField(default=False)
    
    def __unicode__(self):
        if (self.user):
            return "profile with username:%s and email:%s" % (self.user.username, self.user.email)
    
    def owner(self):
        '''
        will retrieve all owners of the instance
        '''   
        #list that will hold instance owners
        owner = []
        try: 
            owner.append(self.user.username)
        except: 
            return []
        
        return owner
    
class Score(LtgModel):
    '''
    will be used as abstract class for the other score models
    '''
    score = models.PositiveSmallIntegerField()
    user_profile = models.ForeignKey(UserProfile)
    date = models.DateTimeField()
    
    class Meta:
        abstract = True
    
class UserScore(Score):
    '''
    will hold user scores history
    '''
     
class UserConceptScore(Score):
    '''
    will hold user concept scores history for user
    '''
    concept = models.ForeignKey(Concept)
    
    def __unicode__(self):
        return "concept:%s with score:%d for user:%s" % (self.concept.title, self.score, self.user_profile.user.email)
    
class UserSectionScore(Score):
    '''
    will hold user section scores history for user
    '''
    section = models.ForeignKey(Section)
    
    def __unicode__(self):
        return "section:%s with score:%d for user:%s" % (self.section.title, self.score, self.user_profile.user.email)
   

class Tutor(object):
    '''
    will hold the tutor object
    '''
    def __init__(self, **kwargs):
        self.id = kwargs.get('id',None)
        self.first_name = kwargs.get('first_name',None)
        self.last_name = kwargs.get('last_name',None)
        self.file_upload = kwargs.get('file_upload',None)
        self.email = kwargs.get('email',None)
        self.skype_id = kwargs.get('skype_id',None)
        self.tutor_description = kwargs.get('tutor_description',None)
        self.tutor_rate = kwargs.get('tutor_rate',None)
        self.tutor_video = kwargs.get('tutor_video',None)
        self.tutor_speciality = kwargs.get('tutor_speciality',None)
        self.tutor_groups = kwargs.get('tutor_groups',None)
        self.country = kwargs.get('country',None)
    
    
class SectionManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)
        
        
class Question(LtgModel):
    '''
    will hold the question model
    '''
    index = models.IntegerField(unique=True)
    answer = models.PositiveSmallIntegerField(choices=ANSWER)
    attempts = models.ManyToManyField(UserProfile, through='Attempt')
    concepts = models.ManyToManyField(Concept)
    sections = models.ManyToManyField(Section)
    
    def __unicode__(self):
        return str(self.index)
    
    @cached_property
    def time_statistics(self):
        '''
        iterate over all attempts for a question and calc
        the mean and std time.
        @return time_statistics list : list containing dicts with statistics for each attempt
        '''
        # init params
        time_statistics = []
        attempt_num = 1
        is_attempt_valid = True
        # query set to hold all the attempts for the current question (query set not evaluated yet)
        question_attempt_qs = Attempt.objects.filter(question_id = self.id)
        # loop while there is an attempt for the question or attempt num is up to 5
        while (is_attempt_valid and attempt_num <= MAX_ALGORITHM_ATTEMPTS):
            # if attempt exists for the question, iterate over all attempts for the question and clac the statistics
            if question_attempt_qs.filter(attempt = attempt_num).exists():
                # will hold the times for each attempt
                durations_per_attempt = []
                for duration_per_attempt in question_attempt_qs.filter(attempt=attempt_num).values_list('duration',flat=True):
                    durations_per_attempt.append(duration_per_attempt.total_seconds())
                # calc time statistics per attempt 
                attempt = {}
                attempt['attempt'] = attempt_num
                attempt['avg'] = numpy.mean(durations_per_attempt)
                attempt['std'] = numpy.std(durations_per_attempt)
                # append to time statistics list
                time_statistics.append(attempt)
                # update attempt number
                attempt_num += 1
            else:
                is_attempt_valid = False
        
        return time_statistics
    
    @cached_property
    def percentage_score_statistics(self):
        ''' 
        calc score and statistics for each attempt of the question
        @return list: each object in the list will contain a dict with values:
        attempt : int ,
        percentage_right : float, 
        wrong_answers_percentage : dict which contains percentage for each wrong answer, 
        score : int
        '''
        # init params
        percentage_score_statistics = []
        attempt_num = 1
        is_attempt_valid = True
        # query set to for all the attempts for the current question (query set not evaluated yet)
        question_attempt_qs = Attempt.objects.filter(question_id = self.id)
        # loop while there is an attempt for the question or attempt num is up to 5
        while (is_attempt_valid and attempt_num <= MAX_ALGORITHM_ATTEMPTS):   
            total_answers = question_attempt_qs.filter(attempt=attempt_num).count()
            # if there were no answers for the question at this attempt exit the loop
            if (total_answers == 0):
                is_attempt_valid = False
            # if there were attempts for the question, calc their score and percentage statistics for this attempt
            else:
                # clac percentage right
                right_answers = question_attempt_qs.filter(attempt=attempt_num,answer = self.answer).count()
                percentage_right_per_attempt =  ((float(right_answers)/total_answers) * 100)
                # calc percentage wrong per answer
                total_wrong_answers = total_answers - right_answers
                wrong_answers_percentage = self._wrong_answers_percentage(total_wrong_answers,attempt_num)
                # calc score for the attempt
                score = self._score(percentage_right_per_attempt)
                # populate our attempt dict
                attempt = {}
                attempt['attempt'] = attempt_num
                attempt['percentage_right'] = percentage_right_per_attempt
                attempt['wrong_answers_percentage'] = wrong_answers_percentage
                attempt['score'] = score
                # append results to the statistics list
                percentage_score_statistics.append(attempt)
                # update attempt number
                attempt_num += 1
        
        return percentage_score_statistics
    
    def _wrong_answers_percentage(self, total_wrong_answers, attempt):
        '''
        will return dictionary with percentage per wrong answer
        @param total_wrong_answers: total wrong answers for the question
        @param attempt : the attempt we're calculation the statistics for
        @return dict: a dictionary containing the percentage of each wrong answer
        '''
        # dictionary for the wrong answers percentage
        wrong_answers_percentage = {}
        # populate wrong answers list
        wrong_answers = []
        for answer in ANSWER:
            if answer[0] != self.answer:
                wrong_answers.append(answer)
        # if there are on wrong answer for the question return dict will all 0 
        if (total_wrong_answers == 0):
            for wrong_answer in wrong_answers:
                wrong_answers_percentage[wrong_answer[1]] = 0
        # if there are calc it
        else:
            # query set for specific attempt and question
            question_attempt_qs = Attempt.objects.filter(question_id = self.id, attempt = attempt)
            # calc wrong answers percentage
            for wrong_answer in wrong_answers:
                num_wrong_answers = question_attempt_qs.filter(answer = wrong_answer[0]).count()
                wrong_answers_percentage[wrong_answer[1]] = (float(num_wrong_answers)/total_wrong_answers) * 100
            
        return wrong_answers_percentage
    
    def _score(self,percentage):
        '''
        get percentage , turn it to percentile, and convert it to the question score.
        @param percentage : the percentage to calc the score for 
        @return: int - question score
        '''
        # get percentile
        percentile = 100 - percentage
        # get percentile and score edges for the interpolation
        percentile_ceil = ScoreTable.objects.filter(percentile__gte = percentile).first().percentile
        percentile_floor = ScoreTable.objects.filter(percentile__lte = percentile).last().percentile
        score_ceil = ScoreTable.objects.get(percentile = percentile_ceil).score
        score_floor = ScoreTable.objects.get(percentile = percentile_floor).score
        # allocate new lists to hold the x,y coordinates (i.e percentile and score coordinates)
        percentile_data_points, score_data_points = [],[]
        percentile_data_points.extend([percentile_floor,percentile_ceil])
        score_data_points.extend([score_floor,score_ceil])
        # clac score based on linear interpolation
        question_score = numpy.interp(percentile, percentile_data_points, score_data_points)
        # round the score 
        return int(round(question_score))
     
    
class Attempt(LtgModel):
    '''
    will hold an attempt of a question by a user
    '''
    user_profile = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question)
    attempt = models.PositiveIntegerField()
    answer = models.PositiveSmallIntegerField(choices=ANSWER)
    duration = TimedeltaField()
    
    def __unicode__(self):
        if (self.question and self.user_profile):
            return "Attempt no.%d, on question no.%d, for user:%s" % (self.attempt, self.question.index, self.user_profile.user.email)

    class Meta(LtgModel.Meta):
        unique_together = (("user_profile", "question","attempt"),)
        index_together = [["question", "attempt"],]
        
class ScoreTable(models.Model):
    '''
    will hold the total score table which translates
    percentile to score
    '''
    percentile = models.DecimalField(max_digits=5,decimal_places=2)
    score = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return "percentile:%.2f , score:%d" % (self.percentile,self.score)
        
#===============================================================================
# end tables - models
#===============================================================================


#===============================================================================
# begin signals
#===============================================================================

def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper

@disable_for_loaddata
def create_api_key_wrapper(sender,**kwargs):
    '''
    will wrap the original create_api_key func in order
    to prevent post save signal while using fixtures in testing since
    causes integration error.
    '''
    create_api_key(sender,**kwargs)
    
# get a user profile for user, or create it if doesn't exist
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# on user save, create an api key for it
models.signals.post_save.connect(create_api_key_wrapper, sender=User)

#===============================================================================
# end signals
#===============================================================================



