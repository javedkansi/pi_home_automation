from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from dateutil import parser
import logging
import datetime as dt
import requests
import pytz

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *
from utils.http_server import *

# read config file
map = read_config("config.yaml", "SCHEDULER")

logging.basicConfig(filename='log/application.log', filemode='a', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)


lightsOffJob = None
lightsOnJob = None
countToSkipMotorOn = 0
sunriseTime = None
sunsetTime = None
lightsOffTime = None
lightsOnTime = None
lightsOnTime = None


class SchedulerServer(JKHttpHandler):
    def do_GET(self):
        params = parse_query_params(self)

        global countToSkipMotorOn

        # for testing purposes only. calls the 'motor on' event if this param is present
        if params.get('test_motor_on'):
            turn_water_motor_on()

        # override the number of times 'motor on' event should be skipped
        if params.get('skip_motor_on'):
            countToSkipMotorOn = int(params.get('skip_motor_on')[0])

        response = "Sunrise: " + sunriseTime.strftime("%H:%M:%S")
        response += "\nSunset: " + sunsetTime.strftime("%H:%M:%S")
        response += "\nLights Off: " + lightsOffTime.strftime("%H:%M:%S")
        response += "\nLights On: " + lightsOnTime.strftime("%H:%M:%S")
        response += "\nTimes to skip motor on: " + str(countToSkipMotorOn)

        self._set_headers()
        self.wfile.write(response)


def turn_lights_on():
    logging.warning("Turning lights on...")
    lights_on()


def turn_lights_off():
    logging.warning("Turning lights off...")
    lights_off()


def turn_water_motor_on():
    global countToSkipMotorOn

    if countToSkipMotorOn > 0:
        countToSkipMotorOn -= 1
        logging.warning("Not going to turn on water motor. Current count to skip motor on is " + str(countToSkipMotorOn))

    else:
        logging.warning("Turning the water motor on...")
        water_motor_on()


def run_hourly_job():
    logging.warning("Running hourly job...")

    # check the current time and determine whether the lights should be on
    # at this time or they should be off and execute appropriate action based on that
    check_lights_with_current_time()

    # turn water motor off on hourly basis
    turn_water_motor_off()

    logging.warning("Hourly job executed...")


def check_lights_with_current_time():
    global lightsOffTime, lightsOnTime
    currenttime = datetime.datetime.now().time()

    # check the current time and determine whether the lights should be on
    # at this time or they should be off and execute appropriate action based on that
    if (currenttime.hour > lightsOnTime.hour or (currenttime.hour == lightsOnTime.minute and currenttime.minute >= lightsOnTime.minute)) \
            or (currenttime.hour < lightsOffTime.hour or (currenttime.hour == lightsOffTime.hour and currenttime.minute < lightsOffTime.minute)):
        logging.warning("Turning lights on based on current time...")
        turn_lights_on()
    else:
        logging.warning("Turning lights off based on current time...")
        turn_lights_off()


def turn_water_motor_off():
    logging.warning("Turning the water motor off...")
    water_motor_off()


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

    global sunriseTime, sunsetTime, lightsOffTime, lightsOnTime

    sunriseTime = serverTimezone.localize(srtime).astimezone(pakistanTz)
    sunsetTime = serverTimezone.localize(sstime).astimezone(pakistanTz)

    send_lcd_screen_request("SR: " + sunriseTime.strftime("%H:%M:%S") + "\nSS: " + sunsetTime.strftime("%H:%M:%S"))

    lightsOffTime = sunriseTime - dt.timedelta(minutes=map.get("TIME_BEFORE_SUNRISE"))
    lightsOnTime = sunsetTime - dt.timedelta(minutes=map.get("TIME_BEFORE_SUNSET"))

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


if __name__ == "__main__":
    # non blocking background scheduler
    scheduler = BackgroundScheduler()

    # job to schedule lights on/off job on a daily basis based on sunrise and sunset
    lightsSchedulingJob = scheduler.add_job(sunset_sunrise_job_scheduler, 'cron', hour=12, id='Lights Scheduler')

    # job that runs every hour and performs some activities like turing off water motor or turning off/on lights etc
    hourlyWaterMotorOffJob = scheduler.add_job(run_hourly_job, 'cron', hour='*/1', minute=5,
                                               id='Hourly water motor off')

    # water motor job every 4 hours for 5mins
    waterMotorOnJob = scheduler.add_job(turn_water_motor_on, 'cron', hour='1,5,9,13,17,21', minute=15,
                                        id='Water motor on job')
    waterMotorOffJob = scheduler.add_job(turn_water_motor_off, 'cron', hour='1,5,9,13,17,21', minute=20,
                                         id='Water motor off job')

    # run the job once to schedule after a restart
    sunset_sunrise_job_scheduler()
    scheduler.start()

    # run hourly job once at the start of the application
    run_hourly_job()

    # start the http server to listen to commands
    run_http_server(handler_class=SchedulerServer, port=map.get("SERVER_PORT"))
