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
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,\
    BaseUserManager
import logging
from django.utils.timezone import utc
from timedelta.fields import TimedeltaField
from django.utils import timezone
import uuid
from ltg_backend_app import settings

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

def _createHash():
    return uuid.uuid4().hex[0:30]

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
    
class LtgUserManager(BaseUserManager):
    
    def _create_user(self, email, password,is_staff,is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_staff = is_staff,
            is_superuser = is_superuser,
            date_joined=now,
            last_login=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_user(self, email, password=None,**extra_fields):
        """
        Creates and saves a user with the given email and password.        
        User will not have admin site access.
        """
        return self._create_user(email, password, False,False, **extra_fields)
        
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Superuser will have admin site access and all permissions.
        """
        return self._create_user(email,password, True,True, **extra_fields)


class LtgUser(AbstractBaseUser,PermissionsMixin):
    
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    username = models.CharField(max_length=30, default=_createHash)
    uuid = models.CharField(max_length=200,blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False,help_text='Designates whether the user can log into this admin site.')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = LtgUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email
    
class Score(LtgModel):
    '''
    will be used as abstract class for the other score models
    '''
    score = models.PositiveSmallIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    
    
class UserSectionScore(Score):
    '''
    will hold user section scores history for user
    '''
    section = models.ForeignKey(Section)
   

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
    attempts = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Attempt')
    concepts = models.ManyToManyField(Concept)
    sections = models.ManyToManyField(Section)
    
    def __unicode__(self):
        return str(self.index)
    
class Attempt(LtgModel):
    '''
    will hold an attempt of a question by a user
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.ForeignKey(Question)
    attempt = models.PositiveIntegerField()
    answer = models.PositiveSmallIntegerField(choices=ANSWER)
    duration = TimedeltaField()
    

    class Meta(LtgModel.Meta):
        unique_together = (("user", "question","attempt"),)
        index_together = [["question", "attempt"],]
        
class ScoreTable(models.Model):
    '''
    will hold the total score table which translates
    percentile to score
    '''
    percentile = models.DecimalField(max_digits=5,decimal_places=2)
    score = models.PositiveSmallIntegerField()
        
        
class QuestionStatistics(LtgModel):
    '''
    will hold our statistics for each question.
    this table will be updated by the celery periodic tests.
    '''
    question = models.ForeignKey(Question)
    attempt = models.PositiveSmallIntegerField()
    attempts_num = models.IntegerField(default=0)
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
    
class ConceptStatistics(LtgModel):
    '''
    will hold each concept statistics
    '''
    concept = models.ForeignKey(Concept)
    mean_score = models.PositiveSmallIntegerField()
    std_score = models.PositiveSmallIntegerField()
    
    
class SectionStatistics(LtgModel):
    '''
    will hold each section statistics
    '''
    section = models.ForeignKey(Section)
    mean_score = models.PositiveSmallIntegerField()
    std_score = models.PositiveSmallIntegerField()
    
    
#===============================================================================
# end tables - models
#===============================================================================




