#!/usr/bin/env python
# -*- coding: utf8 -*-

import signal
import time

import RPi.GPIO as GPIO

import sys,os
sys.path.append(os.getcwd())

from external import MFRC522
from utils.jk_util import *

map = read_config("config.yaml", "RFID_LISTENER")

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


def wait_for_rfid_input():
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            now = get_current_time()

            # Print UID
            cardUID = str(uid[0]) + "" + str(uid[1]) + "" + str(uid[2]) + "" + str(uid[3])
            print "[" + now + "] - Card read UID: " + cardUID

            if cardUID == map.get("SECURITY_LOCK_UNLOCK_ID"):
                jk_room_lights_toggle()

            elif cardUID == map.get("OUTDOOR_LIGHTS_TOGGLE_ID"):
                lights_on()

            else:
                # Print a two line message
                send_lcd_screen_request(cardUID)

            time.sleep(map.get("SLEEP_BETWEEN_READS_IN_MS"))


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

wait_for_rfid_input()
