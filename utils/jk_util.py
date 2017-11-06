from utils.http_sender import *
import time
import yaml

outdoorLightsStatus = 0;
jkRoomLightsStatus = 1;


def jk_room_lights_toggle():
    send_buzzer_request(0.1, 0.05, 3000, 3)
    send_lcd_screen_request_with_time("JK Lights")
    # send_rf_signal(SECURITY_UNLOCK_CODE)
    send_ir_sender_request("KEY_POWER")

    if jkRoomLightsStatus == 0:
        send_rf_sender_request(map.get("LIGHT_JAVED_ROOM_ON"))
    else:
        send_rf_sender_request(map.get("LIGHT_JAVED_ROOM_OFF"))

    time.sleep(5)


def water_motor_on():
    # incase if learning is required for the controller
    water_motor_off()

    time.sleep(2)
    send_rf_sender_request(map.get("SOCKET_WATER_MOTOR_ON"))


def water_motor_off():
    for x in range(0, 5):
        send_rf_sender_request(map.get("SOCKET_WATER_MOTOR_OFF"))
        time.sleep(0.5)


def lights_on():
    # send_buzzer_request(2, 0.05, 1000, 1)
    # send_lcd_screen_request_with_time("Outdoor Lights")

    send_rf_signal_and_sleep(map.get("LIGHT_JAVED_INDOOR_DOWNSTAIRS_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_JAVED_INDOOR_UPSTAIRS_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_KITCHEN_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_GARDEN_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_GATE_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_PARKING_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_GEEZER_ON"))
    send_rf_signal_and_sleep(map.get("LIGHT_WATER_MOTOR_ON"))

    global outdoorLightsStatus;
    outdoorLightsStatus = 1;


def lights_off():
    send_buzzer_request(2, 0.05, 1000, 1)
    send_lcd_screen_request_with_time("Outdoor Lights")

    send_rf_signal_and_sleep(map.get("LIGHT_JAVED_INDOOR_DOWNSTAIRS_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_JAVED_INDOOR_UPSTAIRS_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_KITCHEN_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_GARDEN_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_GATE_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_PARKING_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_GEEZER_OFF"))
    send_rf_signal_and_sleep(map.get("LIGHT_WATER_MOTOR_OFF"))

    global outdoorLightsStatus;
    outdoorLightsStatus = 0;


def send_rf_signal_and_sleep(signal, duration=0.5):
    from components.rf_transmitter import *
    send_rf_signal(signal)
    time.sleep(duration)


def send_lcd_screen_request_with_time(message):
    now = get_current_time()
    send_lcd_screen_request(now + "\n" + message)


def read_config(filename, categoryName):
    map = {}
    stream = open("config.yaml", "r")
    docs = yaml.load_all(stream)
    for doc in docs:
        for k, v in doc.items():
            if k == categoryName:
                return parse_yaml(v)

    return map


def parse_yaml(docs):
    docMap = {}
    for k, v in docs.items():
        docMap[k] = v
    return docMap


map = read_config("config.yaml", "COMMON")

# if __name__ == "__main__":
# send_lcd_screen_request("How are you?")
# send_buzzer_request(0.25, 0.05, 5000, 10)
# send_rf_sender_request("1488996 1 450")
