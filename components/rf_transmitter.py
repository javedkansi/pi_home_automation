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


if __name__ == "__main__":
    run_http_server(handler_class=RFTransmitterServer, port=map.get("SERVER_PORT"))
