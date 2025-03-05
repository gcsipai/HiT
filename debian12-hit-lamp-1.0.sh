#!/bin/bash

# Debian 12 HiT-LAMP-phpMyadmin-2025 Installation Script

# Update and upgrade the system
echo "Updating and upgrading the system..."
apt update && sudo apt upgrade -y

# Install Tasksel (if not already installed)
echo "Installing Tasksel..."
apt install tasksel -y

# Install LAMP stack using Tasksel
echo "Installing LAMP stack (Apache, MySQL, PHP)..."
tasksel install lamp-server

# Secure MySQL installation
echo "Securing MySQL installation..."
mysql_secure_installation <<EOF
y
your_mysql_root_password
your_mysql_root_password
y
y
y
y
EOF

# Install phpMyAdmin
echo "Installing phpMyAdmin..."
apt install phpmyadmin -y <<EOF
apache2
y
EOF

# Create a symbolic link for phpMyAdmin in the web root
echo "Creating symbolic link for phpMyAdmin..."
ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

# Restart Apache to apply changes
echo "Restarting Apache..."
systemctl restart apache2

# Test PHP installation
echo "Creating PHP info file..."
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php

# Display completion message
echo "LAMP stack and phpMyAdmin installation complete!"
echo "You can access phpMyAdmin at: http://your_server_ip/phpmyadmin"
echo "You can test PHP at: http://your_server_ip/info.php"
