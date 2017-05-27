import datetime

import pytz
import requests


def send_buzzer_request(duration, gap, frequency, times):
    query_args = {'duration': duration, 'gap': gap, 'frequency': frequency, 'times': times}
    url = 'http://localhost:8092'
    send_http_request(url, query_args)


def send_rf_sender_request(signal):
    query_args = {'signal': signal}
    url = 'http://localhost:8090'
    send_http_request(url, query_args)


def send_ir_sender_request(signal):
    query_args = {'signal': signal}
    url = 'http://localhost:8094'
    send_http_request(url, query_args)


def send_lcd_screen_request(message_text):
    query_args = {'message': message_text}
    url = 'http://localhost:8091'
    send_http_request(url, query_args)


def send_mobile_status_request(status):
    query_args = {'mobile_status': 0}
    url = 'http://localhost:8093'
    send_http_request(url, query_args)


def send_http_request(url, query_args):
    try:
        print("[" + get_current_time() + "] - Sending request to: " + url + ", " + str(query_args))
        requests.get(url, params=query_args)
    except Exception as inst:
        print("Unable to send request to %s. %s: %s" % (url, type(inst), inst))


def get_current_time():
    return datetime.datetime.now(pytz.timezone("Asia/Karachi")).strftime("%d/%m %I:%M:%S%p")


if __name__ == "__main__":
    # send_lcd_screen_request("How are you?")
    # send_buzzer_request(0.25, 0.05, 5000, 10)
    send_rf_sender_request("1488996 1 450")
