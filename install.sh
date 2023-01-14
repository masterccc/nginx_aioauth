#!/bin/bash

echo "Start installing nginx_aioauth ..."

INSTALL_DIR="/home/${USER}/deploy/apps/nginx_aioauth"

[[ ! -d "$INSTALL_DIR" ]] && mkdir -p "$INSTALL_DIR"

cd "$INSTALL_DIR"

rm -fr venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ---  Root is used below this line --- #

sudo -v
sudo cp -r www/* /var/www/html/
sudo cp nginx_aioauth.service /etc/systemd/system/
sudo sed -i 's/###USERNAME###/'${USER}'/g' /etc/systemd/system/nginx_aioauth.service
sudo systemctl daemon-reload
sudo systemctl enable nginx_aioauth.service


