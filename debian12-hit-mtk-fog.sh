#!/bin/bash

#  Debian 12 HiT-FOG Installation Script

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root."
  exit 1
fi

# Update and upgrade the system
echo "Updating and upgrading the system..."
apt update && apt upgrade -y

# Install required dependencies
echo "Installing required dependencies..."
apt install -y wget git apache2 php-fpm php-cli php-mysql php-curl php-gd php-mbstring php-xml php-zip mariadb-server mariadb-client tftpd-hpa nfs-kernel-server vsftpd net-tools

# Download and install FOG
echo "Downloading and installing FOG..."
cd /opt
wget https://github.com/FOGProject/fogproject/archive/refs/tags/1.5.9.tar.gz -O fogproject-1.5.9.tar.gz
tar -xvzf fogproject-1.5.9.tar.gz
cd fogproject-1.5.9/bin
./installfog.sh

# During the installation, the script will prompt for configuration options.
# Ensure you select the following:
# - Do NOT install the FOG DHCP server (choose 'N' when prompted).
# - Use the existing DHCP server (if you have one).
# - Configure the database settings as needed (defaults are usually fine).

# Configure Apache for FOG
echo "Configuring Apache for FOG..."
a2enconf fog
a2enmod rewrite
systemctl restart apache2

# Configure NFS for FOG
echo "Configuring NFS for FOG..."
echo "/images *(ro,sync,no_wdelay,insecure_locks,no_root_squash,insecure)" > /etc/exports
systemctl restart nfs-kernel-server

# Configure TFTP for FOG
echo "Configuring TFTP for FOG..."
sed -i 's/^TFTP_DIRECTORY="\/srv\/tftp"/TFTP_DIRECTORY="\/tftpboot"/g' /etc/default/tftpd-hpa
systemctl restart tftpd-hpa

# Configure FTP for FOG
echo "Configuring FTP for FOG..."
sed -i 's/^#local_enable=YES/local_enable=YES/g' /etc/vsftpd.conf
sed -i 's/^#write_enable=YES/write_enable=YES/g' /etc/vsftpd.conf
systemctl restart vsftpd

# Configure MariaDB for FOG
echo "Configuring MariaDB for FOG..."
mysql -u root -e "CREATE DATABASE fog;"
mysql -u root -e "CREATE USER 'fog'@'localhost' IDENTIFIED BY 'fogpassword';"
mysql -u root -e "GRANT ALL PRIVILEGES ON fog.* TO 'fog'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

# Restart services
echo "Restarting services..."
systemctl restart apache2
systemctl restart mariadb
systemctl restart tftpd-hpa
systemctl restart nfs-kernel-server
systemctl restart vsftpd

# Finalize FOG installation
echo "Finalizing FOG installation..."
cd /opt/fogproject-1.5.9/bin
./installfog.sh

echo "FOG Server installation complete!"
echo "Access the FOG web interface at http://your-server-ip/fog"
