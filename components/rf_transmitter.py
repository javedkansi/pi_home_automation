#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import with_statement

from subprocess import call
from threading import Lock

import sys,os
sys.path.append(os.getcwd())

from utils.http_server import *
from utils.jk_util import read_config

map = read_config("config.yaml", "RF_TRANSMITTER")

rfSenderLock = Lock()


class RFTransmitterServer(JKHttpHandler):
    def do_GET(self):
        params = parse_query_params(self)

        signal = params.get('signal')[0]
        send_rf_signal(signal)

        self._set_headers()
        self.wfile.write("Ok")


def send_rf_signal(signal):
    global rfSenderLock
    with rfSenderLock:
        # time.sleep(1.0)
        call(map.get("CODE_SEND_BINARY_PATH") + " " + signal, shell=True)
        # time.sleep(0.5)


# # Command to unlock security system
# # sudo /home/pi/test/433Utils/RPi_utils/codesend 1488996 1 450
# CODE_SEND_BINARY_PATH = "/home/pi/test/433Utils/RPi_utils/codesend"
#
# # RF Codes
# SECURITY_UNLOCK_CODE = "1488996 1 450"
# SECURITY_LOCK_CODE = "1488994 1 450"
# LIGHT_JAVED_ROOM = "5731647 1 235"
# LIGHT_JAVED_ROOM_FAN = "5731824 1 235"
# LIGHT_WATER_MOTOR = "5731779 1 235"
# LIGHT_GEEZER = "5731644 1 235"
# LIGHT_MAIN_DOOR = "5731599 1 235"
# LIGHT_PARKING = "5731788 1 235"
# LIGHT_GATE = "5731632 1 235"
# LIGHT_GARDEN = "5731596 1 235"
#
# # [25/02 10:09:20AM] - Received[25] on PIN 2. Code: 15080663. Delay: 312
# # [25/02 10:09:27AM] - Received[26] on PIN 2. Code: 15080671. Delay: 312
# SOCKET_WATER_MOTOR_ON = "15080671 1 312"
# SOCKET_WATER_MOTOR_OFF = "15080663 1 312"

if __name__ == "__main__":
    run_http_server(handler_class=RFTransmitterServer, port=map.get("SERVER_PORT"))
