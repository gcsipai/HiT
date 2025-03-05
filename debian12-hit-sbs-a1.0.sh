#!/bin/bash

# Debian 12 HiT-SBS-Alpha1 Installation Script

# Update and upgrade the system
echo "Updating and upgrading the system..."
apt update && apt upgrade -y

# Install required packages
echo "Installing required packages..."
apt install -y samba smbclient winbind libnss-winbind libpam-winbind krb5-user swat cups samba-vfs-modules samba-dsdb-modules samba-terminal smb4k cockpit nextcloud

# Configure Kerberos (optional, but recommended for Samba AD DC)
echo "Configuring Kerberos..."
dpkg-reconfigure krb5-config

# Provision Samba as an Active Directory Domain Controller
echo "Provisioning Samba as an Active Directory Domain Controller..."
samba-tool domain provision --use-rfc2307 --interactive

# Enable and start Samba services
echo "Enabling and starting Samba services..."
systemctl enable smbd nmbd winbind samba-ad-dc
systemctl start smbd nmbd winbind samba-ad-dc

# Configure SWAT (Samba Web Administration Tool)
echo "Configuring SWAT..."
echo "swat stream tcp nowait.400 root /usr/sbin/swat swat" >> /etc/inetd.conf
systemctl restart openbsd-inetd

# Configure CUPS (Print Server)
echo "Configuring CUPS..."
usermod -aG lpadmin admin
systemctl enable cups
systemctl start cups

# Install Samba Terminal GUI (Optional)
echo "Installing Samba Terminal GUI..."
apt install -y samba-gtk

# Install and configure Nextcloud
echo "Installing and configuring Nextcloud..."
apt install -y nextcloud
echo "Nextcloud installation complete. Access it via http://your-server-ip/nextcloud"

# Restart services
echo "Restarting services..."
systemctl restart smbd nmbd winbind samba-ad-dc cups

# Display completion message
echo "Installation and configuration complete!"
echo "Samba AD DC, SWAT, CUPS, Samba Terminal GUI, and Nextcloud are now installed."
echo "Access SWAT at http://your-server-ip:901"
echo "Access Nextcloud at http://your-server-ip/nextcloud"
