# -*- coding: utf-8 -*-
'''
contains the db models
Created on November 7th, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
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

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================


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
    uuid = models.CharField(max_length=200, default=None,unique=True)
    
    def __unicode__(self):
        return self.user.email
    
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
    will hold our tutor object
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
        
    
    
#===============================================================================
# end tables - models
#===============================================================================


#===============================================================================
# begin signals
#===============================================================================

# get a user profile for user, or create it if doesn't exist
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# on user save, create an api key for it
models.signals.post_save.connect(create_api_key, sender=User)

#===============================================================================
# end signals
#===============================================================================



