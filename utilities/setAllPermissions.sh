#!/bin/bash

# sudo chmod a+w /home/pi/local/.spenv
sudo chmod a+w /home/pi/local/local.json
sudo chmod -R a+w /home/pi/local/www
sudo chmod +x /home/pi/solar-server/charge-controller/csv_datalogger.py
sudo chmod a+w /home/pi/solar-server/frontend/index.html
sudo chmod +x /home/pi/solar-server/utilities/update.sh

echo "Permissions set for local www directory, local.json, deviceList.json, update_ip2.sh, csv_datalogger.py, and index.html"
