#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import with_statement
from threading import Lock
from subprocess import call

import sys,os
sys.path.append(os.getcwd())

from utils.http_server import *
from utils.jk_util import *

# read config file
map = read_config("config.yaml", "IR_TRANSMITTER")

irSenderLock = Lock()


class IRTransmitterServer(JKHttpHandler):
    def do_GET(self):
        params = parse_query_params(self)

        signal = params.get('signal')[0]
        send_ir_signal(signal)

        self._set_headers()
        self.wfile.write("Ok")


def send_ir_signal(signal):
    global irSenderLock
    with irSenderLock:
        # time.sleep(1.0)
        call(CODE_SEND_BINARY_PATH + " " + signal, shell=True)
        # time.sleep(0.25)


# Command for tv volume up
# irsend SEND_ONCE samsung4 KEY_VOLUMEUP
CODE_SEND_BINARY_PATH = "irsend SEND_ONCE samsung2"

if __name__ == "__main__":
    run_http_server(handler_class=IRTransmitterServer, port=map.get("SERVER_PORT"))
