import logging
import subprocess
import time

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *

# read config file
map = read_config("config.yaml", "MOBILE")

logging.basicConfig(filename='log/application.log', filemode='a', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)


def detect_mobile():
    isMobileOnNetwork = -1
    notDetectedCount = 0

    while True:
        time.sleep(1)
        p = subprocess.Popen(map.get("ARP_SCAN_COMMAND"), stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        if output:
            notDetectedCount = 0
        else:
            notDetectedCount += 1

        if notDetectedCount >= 10 and check_ping() == False:

            if isMobileOnNetwork == 1:
                # turn lights etc off here
                jk_room_lights_toggle()
                send_mobile_status_request(0)

            isMobileOnNetwork = 0
            logging.warning("Mobile device NOT connected to the wifi network...")


        else:
            isMobileOnNetwork = 1
            logging.warning("Mobile device detected on the wifi network...")


def check_ping():
    sHost = map.get("IP_ADDRESS")
    try:
        output = subprocess.check_output("ping -c 1 " + sHost, shell=True)
    except Exception, e:
        return False

    return True


if __name__ == "__main__":
    detect_mobile()
