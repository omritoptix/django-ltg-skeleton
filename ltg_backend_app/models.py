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
# begin models abstract classes
#===============================================================================

class LtgModel(models.Model):
    '''
    this class will be an abstract class for all my models
    and it will contain common information
    '''
    creation_date = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    modified_data = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0), auto_now=True)
    
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
    uuid = models.CharField(max_length=200, default=None, blank=True, null=True)
    
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

    

#===============================================================================
# end signals
#===============================================================================



