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



