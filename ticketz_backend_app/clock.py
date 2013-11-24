

from apscheduler.scheduler import Scheduler
from ticketz_backend_app.models import *
from dateutil.relativedelta import relativedelta

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def close_deals():
    '''
    deal that passed the valid to should be closed
    '''
    
    print 'Closing deals that passed the valid_to'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)
    
@sched.interval_schedule(minutes=5)
def activate_pending_deals():
    '''
    deals that are pending more than 10 minutes should turn to active
    '''
    
    print 'activating pending deals'
    now = datetime.datetime.now()
    ten_before = now + relativedelta(minutes=-10)
    Deal.objects.filter(creation_date__lte=ten_before, status=1).update(status=2)


sched.start()

while True:
    pass

