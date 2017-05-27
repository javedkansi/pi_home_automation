from __future__ import with_statement

import time
import RPi.GPIO as GPIO

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *
from utils.http_server import *

# read config file
map = read_config("config.yaml", "IR_TRANSMITTER")

class BuzzerServer(JKHttpHandler):
    def do_GET(self):
        params = parse_query_params(self)

        duration = float(params.get('duration')[0])
        gap = float(params.get('gap')[0])
        frequency = int(params.get('frequency')[0])
        times = int(params.get('times')[0])

        buzzer_beep(duration, gap, frequency, times)

        self._set_headers()
        self.wfile.write("Ok")


def buzzer_beep(duration=0.1, gap=0.05, frequency=5000, times=2):
    BUZZER_GPIO_PIN = 26

    for x in range(0, times):
        GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
        GPIO.setup(BUZZER_GPIO_PIN, GPIO.OUT)  # Set pins' mode is output
        # global Buzz # Assign a global variable to replace GPIO.PWM
        Buzz = GPIO.PWM(BUZZER_GPIO_PIN, 5000)  # 440 is initial frequency.

        Buzz.start(50)  # Start Buzzer pin with 50% duty ration

        time.sleep(duration)
        Buzz.stop()  # Stop the buzzer
        GPIO.output(BUZZER_GPIO_PIN, 1)  # Set Buzzer pin to High
        time.sleep(gap)


def buzzer_dual_beep():
    buzzer_beep(0.1)


if __name__ == "__main__":
    run_http_server(handler_class=BuzzerServer, port=map.get("SERVER_PORT"))
