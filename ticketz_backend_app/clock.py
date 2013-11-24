

from apscheduler.scheduler import Scheduler
from ticketz_backend_app.models import *

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def close_deals():
    print 'This job is run every minute.'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)

@sched.cron_schedule(day_of_week='mon-fri', hour=17)
def scheduled_job():
    print 'This job is run every weekday at 5pm.'

sched.start()

while True:
    pass

