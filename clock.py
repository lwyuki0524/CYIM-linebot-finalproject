from apscheduler.schedulers.blocking import BlockingScheduler
from cyimapp.views import modifyUbike
sched = BlockingScheduler()

"""
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
"""
@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/3')
def scheduled_job():
    modifyUbike()
    #print('This job is run every weekday at 5pm.')

sched.start()