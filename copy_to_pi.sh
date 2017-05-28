ssh -t pi@192.168.1.60 "sudo /home/pi/pi_home_automation/stop_all.sh"
scp -r * pi@192.168.1.60:~/pi_home_automation
ssh -t pi@192.168.1.60 "sudo /home/pi/pi_home_automation/start_all.sh"