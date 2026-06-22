#!/bin/sh
LOG="/tmp/sp/mnt/sda1/payload.log"
exec > "$LOG" 2>&1

NVM="/tmp/sp/media/flash/nvm"
SETUP="$NVM/Sunplus/SETUPMENU.ini"
BTCONF="$NVM/goc/bt_conf.ini"

echo "Backup"
cp "$SETUP" "/tmp/sp/mnt/sda1/SETUPMENU.ini.bak"
cp "$BTCONF" "/tmp/sp/mnt/sda1/bt_conf.ini.bak"

echo "SETUPMENU.ini"
sed -i 's/bluetooth.name=Car Bt/bluetooth.name=Car Bt/' "$SETUP"
sed -i 's/SetupWifi.WifiName=Car Bt/SetupWifi.WifiName=Car Bt/' "$SETUP"

echo "bt_conf.ini"
sed -i 's/localname=Car Bt/localname=Car Bt/' "$BTCONF"

echo "WiFi SSID"
sed -i 's/^ssid=Car Bt/ssid=Car Bt/' "$NVM/softap.conf"
grep "ssid=" "$NVM/softap.conf"

echo "Check"
grep -E "bluetooth.name|WifiName|localname" "$SETUP" "$BTCONF"

sync && sleep 5 && sync
echo "DONE"