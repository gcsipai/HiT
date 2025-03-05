#!/bin/bash

Debian 12 HiT-LAMP-phpMyadmin-Cockpit-1.2 Installation Script

# Update and upgrade the system
echo "Updating and upgrading the system..."
sudo apt update && sudo apt upgrade -y

# Install Apache2
echo "Installing Apache2..."
sudo apt install -y apache2

# Enable and start Apache2 service
echo "Enabling and starting Apache2 service..."
sudo systemctl enable apache2
sudo systemctl start apache2

# Install PHP 8.2 (or latest available)
echo "Installing PHP 8.2 and common modules..."
sudo apt install -y php php-cli php-fpm php-mysql php-curl php-gd php-mbstring php-xml php-zip

# Install MariaDB
echo "Installing MariaDB..."
sudo apt install -y mariadb-server

# Secure MariaDB installation
echo "Securing MariaDB installation..."
sudo mysql_secure_installation <<EOF
y
password
password
y
y
y
y
EOF

# Create a test database and user (optional)
echo "Creating a test database and user..."
sudo mysql -u root -ppassword <<EOF
CREATE DATABASE testdb;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testpassword';
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
EOF

# Install phpMyAdmin
echo "Installing phpMyAdmin..."
sudo apt install -y phpmyadmin

# Configure phpMyAdmin to work with Apache2
echo "Configuring phpMyAdmin..."
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2

# Install Cockpit and Cockpit Apache2 module
echo "Installing Cockpit and Cockpit Apache2 module..."
sudo apt install -y cockpit cockpit-apache

# Enable and start Cockpit service
echo "Enabling and starting Cockpit service..."
sudo systemctl enable cockpit.socket
sudo systemctl start cockpit.socket

# Allow Cockpit through the firewall (if enabled)
echo "Allowing Cockpit through the firewall..."
sudo ufw allow 9090/tcp

# Restart Apache2 to apply changes
echo "Restarting Apache2..."
sudo systemctl restart apache2

# Display installation summary
echo "Installation complete!"
echo "Apache2 is running on: http://localhost/"
echo "phpMyAdmin is available at: http://localhost/phpmyadmin/"
echo "Cockpit is available at: https://localhost:9090/"
echo "MariaDB test database:"
echo "  Database: testdb"
echo "  Username: testuser"
echo "  Password: testpassword"
