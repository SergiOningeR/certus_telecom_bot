#!/bin/bash
# Certus Bot Deployment Script

echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-dev python3-venv libmysqlclient-dev build-essential mysql-server

echo "Setting up MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS certus_telecom;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'certus_bot'@'localhost' IDENTIFIED BY 'strongpassword';"
sudo mysql -e "GRANT ALL PRIVILEGES ON certus_telecom.* TO 'certus_bot'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "Creating bot user..."
sudo useradd -m -d /opt/certus_telecom_bot -s /bin/bash botuser

echo "Cloning repository..."
sudo -u botuser git clone https://github.com/SergiOningeR/certus_telecom_bot.git /opt/certus_telecom_bot

echo "Setting up virtual environment..."
sudo -u botuser python3 -m venv /opt/certus_telecom_bot/venv
sudo -u botuser /opt/certus_telecom_bot/venv/bin/pip install -r /opt/certus_telecom_bot/requirements.txt

echo "Initializing database..."
sudo -u botuser /opt/certus_telecom_bot/venv/bin/python -m database.setup_db

echo "Setting up systemd service..."
sudo cp /opt/certus_telecom_bot/deploy/certus_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable certus_bot.service
sudo systemctl start certus_bot.service

echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable certus_bot.service
sudo systemctl enable certus_admin.service
sudo systemctl start certus_bot
sudo systemctl start certus_admin

echo "Configuring Nginx as reverse proxy..."
sudo apt install -y nginx
sudo cp /opt/certus_telecom_bot/deploy/nginx.conf /etc/nginx/sites-available/certus
sudo ln -s /etc/nginx/sites-available/certus /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx

echo "Deployment complete!"
