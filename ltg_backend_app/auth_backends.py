'''
contains custom authentication backend of our application
Created on April 16, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from ltg_backend_app.models import LtgUser
from django.contrib.auth import get_user_model

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin custom authentication backends
#===============================================================================

class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """
    
    def authenticate(self, email=None, password=None):
        """ Authenticate a user based on email address """
        try:
            User = get_user_model()
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 
        
#===============================================================================
# end custom authentication backends
#===============================================================================
