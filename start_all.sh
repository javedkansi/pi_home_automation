if [ "$(id -u)" != "0" ]; 
  then echo "Please run as root"
  exit
fi

#python /home/pi/pi_home_automation/components/buzzer.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/components/lcd_screen.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/components/rf_transmitter.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/components/ir_transmitter.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/components/rf_receiver.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/components/rfid_listener.py &>> /home/pi/pi_home_automation/log/console.log &
#python /home/pi/pi_home_automation/mobile/mobile_detector.py &>> /home/pi/pi_home_automation/log/console.log &
python /home/pi/pi_home_automation/scheduler/scheduler.py &>> /home/pi/pi_home_automation/log/console.log &
