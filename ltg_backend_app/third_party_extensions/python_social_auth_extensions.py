'''
social auth pipeline extension 
Created on May 21st, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from social.pipeline.user import USER_FIELDS
from django.contrib.auth import get_user_model
import uuid
from ltg_backend_app.tasks import create_hubspot_contact
from ltg_backend_app import settings

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin pipeline extensions
#===============================================================================

def create_user(strategy, details, response, uid, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                        for name in strategy.setting('USER_FIELDS',
                                                      USER_FIELDS))
    if not fields:
        return

    # check that email is present
    if 'email' not in fields or not fields['email']:
        return {}
    
    # get the email and generate password for the user
    email = fields['email']
    del fields['email']
    User = get_user_model()
    password = uuid.uuid4().hex[0:16]
    
    # create the user 
    user = User.objects.create_user(email=email, password=password, **fields)
    # create the user in hubspot
    create_hubspot_contact.delay(user=user,list_id=settings.HUBSPOT_USERS_LIST_ID)
    
    return {
        'is_new': True,
        'user': user
    }
    
#===============================================================================
# end pipeline extensions
#===============================================================================