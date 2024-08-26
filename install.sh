#!/bin/bash

echo 'Installing Python and necessary packages...'
apt update
apt install -y python3-dev python3-venv python3-pip

echo 'Creating systemd service symlink...'
ln -s /opt/wb-shtyl/systemd/wb-shtyl.service /etc/systemd/system/wb-shtyl.service
systemctl daemon-reload
systemctl enable wb-shtyl.service

echo 'Setting up virtual environment...'
python3 -m venv /opt/wb-shtyl/venv
source /opt/wb-shtyl/venv/bin/activate

echo 'Installing Python dependencies...'
pip install -r /opt/wb-shtyl/requirements.txt
deactivate

echo 'Copying .env.example to .env...'
cp /opt/wb-shtyl/.env.example /opt/wb-shtyl/.env

echo '---------------------------------------------------------------------------'
echo 'Installation complete!'
echo 'Please configure the .env file located at: /opt/wb-shtyl/.env'
echo 'To start the wb-shtyl service, use: systemctl start wb-shtyl.service'
