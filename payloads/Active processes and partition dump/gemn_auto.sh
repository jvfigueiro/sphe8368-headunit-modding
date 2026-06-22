#!/bin/sh

LOG="/tmp/sp/mnt/sda1/TAR_BACKUP.txt"

echo "====================================" > $LOG
echo "Starting dump" >> $LOG
echo "====================================" >> $LOG

tar -czf /tmp/sp/mnt/sda1/nvm_backup.tar.gz /tmp/sp/media/flash/nvm/ /tmp/sp/media/flash/userdata/
echo "[+] System dump completed." >> $LOG

echo -e "\n[+] Active Processes:" >> $LOG
ps >> $LOG

echo "All set. Extraction completed." >> $LOG

sync
sleep 5
sync
sleep 5
