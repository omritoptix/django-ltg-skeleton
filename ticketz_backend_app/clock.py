

from apscheduler.scheduler import Scheduler
from ticketz_backend_app.models import *

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def close_deals():
    print 'Closing deals that passed the valid_to'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)


sched.start()

while True:
    pass

