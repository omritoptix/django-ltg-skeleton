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
from django.utils import timezone
import uuid
from ltg_backend_app import settings

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
    """
    Will represent our custom user.
    reference to this model should be done via get_user_model() method of django auth.
    """ 
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
    
#===============================================================================
# end tables - models
#===============================================================================




