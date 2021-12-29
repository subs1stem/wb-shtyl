#!/bin/bash
apt install python3-dev

echo 'Creating service...'
cp -u -r service/wb-shtyl.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable wb-shtyl.service

cp -u -r source /mnt/data/etc/wb-shtyl && cd /mnt/data/etc/wb-shtyl || exit

echo 'Installing venv...'
python3 -m venv venv
source venv/bin/activate

echo 'Installing requirements...'
pip install -r requirements.txt
deactivate

echo '--------------------------------------------------------------------'
echo 'Done. Edit the settings.py file at the path /mnt/data/etc/wb-shtyl.'
echo 'Use "systemctl start wb-shtyl.service" for running module.'