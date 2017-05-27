if [ "$(id -u)" != "0" ]; 
  then echo "Please run as root"
  exit
fi

#kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/buzzer.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/lcd_screen.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/rf_transmitter.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/ir_transmitter.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/rf_receiver.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/components/rfid_listener.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
kill -9 $(ps aux | grep '[p]ython /home/pi/pi_home_automation/mobile/mobile_detector.py' | awk '{print $2}') &>> /home/pi/pi_home_automation/log/application.log
