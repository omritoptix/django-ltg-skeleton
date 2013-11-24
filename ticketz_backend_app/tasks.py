'''
used for celery as periodic tasks

Created November 23rd, 2013
@author: Yariv Katz
@version: 1.0
@copyright: Nerdeez Ltd.
'''

####################
# begin imports 
####################

from celery import task
from ticketz_backend_app.models import *
from datetime import timedelta
from celery.decorators import periodic_task
import datetime
from os import environ
from celery import Celery


####################
# end imports 
####################

# REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost')

# celery = Celery('ticketz_backend_app.tasks', broker=REDIS_URL)


@periodic_task(run_every=timedelta(minutes=1), name='tasks.async_tasks')
def async_tasks():
    '''
    all the application async process will be run here
    '''
    
    # update deals that valid to has passed to be closed
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)
    
    
    