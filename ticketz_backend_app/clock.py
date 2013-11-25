

from apscheduler.scheduler import Scheduler
from ticketz_backend_app.models import *
from dateutil.relativedelta import relativedelta
from tastypie.models import ApiKey
from tastypie.api import Api

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def close_deals():
    '''
    deal that passed the valid to should be closed
    '''
    
    print 'Closing deals that passed the valid_to'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)
    
@sched.interval_schedule(minutes=1)
def active_deals():
    '''
    deal that passed the valid from should be Active
    '''
    
    print 'Change to active deals that passed the valid_from'
    Deal.objects.filter(valid_from__lte=datetime.datetime.now(), valid_to__gt=datetime.datetime.now()).update(status=4)
    
@sched.interval_schedule(minutes=5)
def activate_pending_deals():
    '''
    deals that are pending more than 10 minutes should turn to active
    '''
    
    print 'activating pending deals'
    now = datetime.datetime.now()
    ten_before = now + relativedelta(minutes=-10)
    Deal.objects.filter(creation_date__lte=ten_before, status=1).update(status=2)
    
@sched.interval_schedule(hours=24)
def delete_old_api_keys():
    '''
    api keys that are older than 24 hours should be deleted
    '''
    
    print 'Deleting old api keys'
    now = datetime.datetime.now()
    day_before = now + relativedelta(hours=-24)
    ApiKey.objects.filter(created__lt=day_before).delete()
    



sched.start()

while True:
    pass

