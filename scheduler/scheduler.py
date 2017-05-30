from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from dateutil import parser
import datetime as dt
import requests
import pytz

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *


lightsOffJob = None
lightsOnJob = None


def toggle_lights():
    print "Lights toggled..."
    outdoor_lights_toggle()


def sunset_sunrise_job_scheduler():
    response = requests.get('https://api.sunrise-sunset.org/json?lat=33.725699&lng=73.073496&date=today')
    data = response.json()

    sr = data.get("results").get("sunrise")
    ss = data.get("results").get("sunset")

    srtime = parser.parse(sr)
    sstime = parser.parse(ss)

    serverTimezone = pytz.timezone("UTC")
    pakistanTz = pytz.timezone("Asia/Karachi")

    sunrise = serverTimezone.localize(srtime).astimezone(pakistanTz)
    sunset = serverTimezone.localize(sstime).astimezone(pakistanTz)

    send_lcd_screen_request("SR: " + sunrise.strftime("%H:%M:%S") + "\nSS: " + sunset.strftime("%H:%M:%S"))

    lightsOffTime = sunrise - dt.timedelta(minutes=10)
    lightsOnTime = sunset - dt.timedelta(minutes=10)

    global lightsOffJob
    global lightsOnJob

    if lightsOffJob is not None:
        scheduler.remove_job('Lights Off')

    if lightsOffJob is not None:
        scheduler.remove_job('Lights On')

    lightsOffJob = scheduler.add_job(toggle_lights, 'date', run_date=lightsOffTime, id='Lights Off')
    lightsOnJob = scheduler.add_job(toggle_lights, 'date', run_date=lightsOnTime, id='Lights On')

    scheduler.print_jobs()


scheduler = BlockingScheduler()
job = scheduler.add_job(sunset_sunrise_job_scheduler, 'cron', hour=12, id='Job Scheduler')

sunset_sunrise_job_scheduler()
scheduler.start()
