#!/bin/bash

# Debian 12 HiT-LAMP-phpMyadmin-1.1 Installation Script

# Update and upgrade the system
apt update && apt upgrade -y

# Install Apache2
apt install -y apache2

# Install MariaDB
apt install -y mariadb-server mariadb-client

# Secure MariaDB installation
mysql_secure_installation <<EOF
y
y
your_password
your_password
y
y
y
y
EOF

# Install PHP 8 and required modules
apt install -y php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath

# Install phpMyAdmin
apt install -y phpmyadmin

# Configure phpMyAdmin to work with Apache
ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

# Install Apache2 Admin (Web-based Apache configuration tool)
apt install -y libapache2-mod-php
wget -O /var/www/html/apache2-admin.zip https://github.com/ericmann/apache2-admin/archive/refs/heads/master.zip
unzip /var/www/html/apache2-admin.zip -d /var/www/html/
mv /var/www/html/apache2-admin-master /var/www/html/apache2-admin
rm /var/www/html/apache2-admin.zip

# Set permissions for Apache2 Admin
chown -R www-data:www-data /var/www/html/apache2-admin
chmod -R 755 /var/www/html/apache2-admin

# Enable Apache modules and restart
a2enmod rewrite
systemctl restart apache2

# Print installation details
echo "Installation completed successfully!"
echo "Apache2, MariaDB, PHP 8, phpMyAdmin, and Apache2 Admin are installed."
echo "phpMyAdmin is accessible at http://localhost/phpmyadmin"
echo "Apache2 Admin is accessible at http://localhost/apache2-admin"
