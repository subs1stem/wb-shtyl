# wb-shtyl
Module for integrating the Shtyl UPS into the Wiren Board controller

## Installation
On Wiren Board controller:
```
git clone https://github.com/subs1stem/wb-shtyl.git
cd wb-shtyl
chmod +x install.sh
./install.sh
```

## Usage
Edit the file at the path `/mnt/data/etc/wb-shtyl/settings.py` and use `systemctl start wb-shtyl.service` for running module
