from __future__ import with_statement

import Adafruit_CharLCD as LCD

import sys,os
sys.path.append(os.getcwd())

from utils.jk_util import *
from utils.http_server import *

# read config file
map = read_config("config.yaml", "LCD_SCREEN")

# Raspberry Pi pin configuration:
lcd_rs = 16  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en = 12
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


class LcdScreenServer(JKHttpHandler):
    def do_GET(self):
        params = parse_query_params(self)

        message = params.get('message')[0]
        lcd_message(message)

        self._set_headers()
        self.wfile.write("Ok")


def lcd_message(message):
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)

    lcd.clear()
    lcd.message(message)


if __name__ == "__main__":
    run_http_server(handler_class=LcdScreenServer, port=map.get("SERVER_PORT"))
    lcd_message("Started")
