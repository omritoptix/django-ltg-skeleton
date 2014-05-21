'''
contains the app signals
Created on May 21st, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from functools import wraps
from ltg_backend_app.models import LtgUser
from django.db.models import signals
from tastypie.models import create_api_key

#===============================================================================
# end imports
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
     
# on user save, create an api key for it
signals.post_save.connect(create_api_key_wrapper, sender=LtgUser)
 
#===============================================================================
# end signals
#===============================================================================