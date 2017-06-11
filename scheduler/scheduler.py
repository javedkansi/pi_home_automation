from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from dateutil import parser
import logging
import datetime as dt
import requests
import pytz

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *

# read config file
map = read_config("config.yaml", "SCHEDULER")

logging.basicConfig(filename='log/application.log', filemode='a', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)

lightsOffJob = None
lightsOnJob = None


def turn_lights_on():
    logging.warning("Turning lights on...")
    lights_on()


def turn_lights_off():
    logging.warning("Turning lights off...")
    lights_off()


def sunset_sunrise_job_scheduler():
    logging.warning("Checking sunset/sunrise time to schedule jobs...")

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

    lightsOffTime = sunrise - dt.timedelta(minutes=map.get("TIME_BEFORE_SUNRISE"))
    lightsOnTime = sunset - dt.timedelta(minutes=map.get("TIME_BEFORE_SUNSET"))

    global lightsOffJob
    global lightsOnJob

    if lightsOffJob is not None:
        scheduler.remove_job('Lights Off')

    if lightsOffJob is not None:
        scheduler.remove_job('Lights On')

    lightsOffJob = scheduler.add_job(turn_lights_off, 'cron', hour=lightsOffTime.hour, minute=lightsOffTime.minute, second='0,25,50', id='Lights Off')
    lightsOnJob = scheduler.add_job(turn_lights_on, 'cron', hour=lightsOnTime.hour, minute=lightsOnTime.minute, second='0,25,50', id='Lights On')

    scheduler.print_jobs()
    logging.warning("Lights will be turned off at: " + str(lightsOffTime.hour) + ":" + str(lightsOffTime.minute));
    logging.warning("Lights will be turned on at: " + str(lightsOnTime.hour) + ":" + str(lightsOnTime.minute));


scheduler = BlockingScheduler()
job = scheduler.add_job(sunset_sunrise_job_scheduler, 'cron', hour=12, id='Job Scheduler')

sunset_sunrise_job_scheduler()
scheduler.start()
