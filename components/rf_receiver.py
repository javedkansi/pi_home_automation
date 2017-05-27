import logging
import signal
import thread

from pi_switch import RCSwitchReceiver
from threading import Lock

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *
from utils.http_server import *

# read config file
rfCodeMappings = read_config("config.yaml", "RF_CODE_MAPPINGS")
map = read_config("config.yaml", "RF_RECEIVER")
commonMap = read_config("config.yaml", "COMMON")

continue_reading_rf = True
jkRoomLights = True

logging.basicConfig(filename='log/rf_listener.log', filemode='a', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)

rfListenerLock = Lock()

class RFListenerHttp(JKHttpHandler):
    def do_GET(self):
        global jkRoomLights

        params = parse_query_params(self)
        mobile_status = params.get('mobile_status')[0]

        if mobile_status == "0":
            jkRoomLights = False
            logging.warning("Lights turned off in JK room. Going to read motion sensor to turn on again...")

        self._set_headers()
        self.wfile.write("Ok")


def end_reading(signal, frame):
    print("Stopping RF reader...")
    global continue_reading_rf
    continue_reading_rf = False


def listen_to_rf_signals(pin):
    num = 0
    receiver = RCSwitchReceiver()
    receiver.enableReceive(pin)

    print("")
    print("Waiting for RF signals on PIN %s..." % pin)

    while continue_reading_rf:
        if receiver.available():
            received_value = receiver.getReceivedValue()

            # if str(received_value) in LIGHT_JAVED_ROOM:
            #	logging.warning("Lights toggled in JK room...")
            #	jkRoomLights = not jkRoomLights

            if received_value:
                num += 1

                now = datetime.datetime.now(pytz.timezone("Asia/Karachi")).strftime("%d/%m %I:%M:%S%p")
                print("[" + now + "] - Received[%s] on PIN %s. Code: %s. Delay: %s" % (
                num, pin, received_value, receiver.getReceivedDelay()))

                v = rfCodeMappings.get(received_value)
                if v:
                    global jkRoomLights

                    if v == "JK Room Motion" and jkRoomLights == False:
                        logging.warning("Motion detected and lights are off. Turning them on...")
                        send_rf_sender_request(commonMap.get("LIGHT_JAVED_ROOM"))
                        jkRoomLights = not jkRoomLights

                    send_lcd_screen_request(now + "\n" + v)
                    logging.warning(v)
                    send_buzzer_request(0.08, 0.03, 3000, 3)
                    # time.sleep(1)

            receiver.resetAvailable()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_reading)

if __name__ == "__main__":
    pin = 3
    if len(sys.argv) > 1:
        pin = sys.argv[1]

    if pin == 3:
        thread.start_new_thread(listen_to_rf_signals, (pin,))
        run_http_server(handler_class=RFListenerHttp, port=map.get("SERVER_PORT"))
        print("New thread started to listen on port 8093")
    else:
        listen_to_rf_signals(int(pin))
