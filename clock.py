from apscheduler.schedulers.blocking import BlockingScheduler
from cyimapp.views import modifyUbike
import datetime

sched = BlockingScheduler()

"""
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
"""
@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/3')
def scheduled_job():
    print('This job runs every day */3 min.')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    modifyUbike()
    #print('This job is run every weekday at 5pm.')

sched.start()