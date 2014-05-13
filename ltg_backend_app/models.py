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
# min attempt duration (in sec) in order to be considered in the algorithm
MIN_ATTEMPT_DURATION = 5

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
        
        
class QuestionStatistics(LtgModel):
    '''
    will hold our statistics for each question.
    this table will be updated by the celery periodic tests.
    '''
    question = models.ForeignKey(Question)
    attempt = models.PositiveSmallIntegerField()
    mean_time = TimedeltaField()
    std_time = TimedeltaField()
    percentage_right = models.DecimalField(max_digits=5, decimal_places=2)
    score = models.PositiveSmallIntegerField()
    
    class Meta(LtgModel.Meta):
        unique_together = (("question","attempt"),)
        index_together = [["question", "attempt"],]

class WrongAnswersPercentage(LtgModel):
    '''
    will hold the wrong answers percentage for each (question,attempt) pair
    '''
    answer = models.SmallIntegerField(choices=ANSWER)
    percentage_wrong = models.DecimalField(max_digits=5,decimal_places=2)
    question_statistics = models.ForeignKey(QuestionStatistics)
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



