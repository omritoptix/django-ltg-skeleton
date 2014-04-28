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
        
        
class Question(LtgModel):
    '''
    will hold the question model
    '''
    index = models.IntegerField(unique=True)
    answer = models.PositiveSmallIntegerField(choices=ANSWER)
    attempts = models.ManyToManyField(UserProfile, through='Attempt')
    
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
        # get all the attempts for the current questions
        question_attempt_qs = Attempt.objects.filter(question_id = self.id)
        # loop while there is an attempt for the question
        while (is_attempt_valid):
            # it attempt exists for the question, iterate over all attempts for the question and clac the statistics
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
    def percentage_right(self):
        ''' 
        calc percentage of people who got this question right
        @return float: percentage of people which answered right.
        '''
        total_answers = Attempt.objects.filter(question_id=self.id,attempt=1).count()
        if (total_answers == 0):
            return 100.0
        right_answers = Attempt.objects.filter(question_id=self.id,attempt=1,answer = self.answer).count()
        return ((float(right_answers)/total_answers) * 100)
    
    @cached_property
    def wrong_answers(self):
        '''
        iterate over all the first attempts for each question and calc
        the wrong answers percetange 
        @return: dictionary with answers as keys and percentage of wrong answers as values 
        '''
        # init params
        wrong_ans = {}
        # it attempt exists for the question, iterate over all attempts for the question and calc the statistics
        if Attempt.objects.filter(question_id = self.id,attempt = 1).exists():
            # will hold the number of wrong answers for each option
            wrong_ans = {'A':0,'B':0,'C':0,'D':0,'E':0}
            for attempt in Attempt.objects.filter(question_id=self.id,attempt=1).exclude(answer=self.answer):
                    wrong_ans[attempt.get_answer_display()] += 1
            # delete the right answer key
            del wrong_ans[self.get_answer_display()]
            # total wrong answers
            total_wrong_ans = Attempt.objects.filter(question_id=self,attempt=1).exclude(answer=self.answer).count()
            if (total_wrong_ans == 0):
                return wrong_ans
            # calc wrong answers percentage per answer
            for wrong_ans_key in wrong_ans.keys():
                wrong_ans[wrong_ans_key] = (float(wrong_ans[wrong_ans_key])/total_wrong_ans) * 100
        
        return wrong_ans
    
    @cached_property
    def score(self):
        '''
        get percentage , turn it to percentile, and convert it to the question score. 
        @return: int - question score
        '''
        percentage = self.percentage_right
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
    
class Concept(LtgModel):
    '''
    will hold the concept model
    '''
    title = models.CharField(unique=True,max_length=200)
    questions = models.ManyToManyField(Question)
    
    def __unicode__(self):
        return self.title
    
    @cached_property
    def statistics(self):
        concept_scores = ConceptScore.objects.filter(concept_id = self.id).values_list('score')
        mean = numpy.mean(concept_scores)
        std = numpy.std(concept_scores)
        return {'mean':mean,'std':std}
    
class Section(LtgModel):
    '''
    will hold the section model
    '''
    title = models.CharField(unique=True,max_length=200)
    questions = models.ManyToManyField(Question)
    
    def __unicode__(self):
        return self.title
    
    @cached_property
    def statistics(self):
        section_scores = SectionScore.objects.filter(section_id = self.id).values_list('score')
        mean = numpy.mean(section_scores)
        std = numpy.std(section_scores)
        return {'mean':mean,'std':std}
    
class QuestionSetAttempt(LtgModel):
    '''
    will hold the question set model
    '''    
    concepts = models.ManyToManyField(Concept, through='ConceptScore')
    sections = models.ManyToManyField(Section, through='SectionScore')    
        
    
class ConceptScore(LtgModel): 
    '''
    will hold data regarding the concept for each question set attempt
    '''
    score = models.PositiveSmallIntegerField()
    question_set_attempt = models.ForeignKey(QuestionSetAttempt)
    concept = models.ForeignKey(Concept)
    
    
class SectionScore(LtgModel): 
    '''
    will hold data regarding the section for each question set attempt
    '''
    score = models.PositiveSmallIntegerField()
    question_set_attempt = models.ForeignKey(QuestionSetAttempt)
    section = models.ForeignKey(Section)
     
    
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



