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

####################
# end imports 
####################

@periodic_task(run_every=timedelta(minutes=1), name='tasks.close_deals')
def close_deals():
    '''
    will run every minute and close all the expired deals
    '''
    print 'running celery - close_deals'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)
    
    
    