#!/bin/bash

# Debian 12 HiT-Samba4-SWAT-CUPS-2025 Installation Script

# Update and upgrade the system
echo "Updating and upgrading the system..."
apt update && sudo apt upgrade -y

# Install necessary packages
echo "Installing Samba4 AD DC, SWAT, and CUPS..."
apt install -y samba smbclient winbind libnss-winbind libpam-winbind krb5-user samba-dsdb-modules samba-vfs-modules swat cups

# Backup the original Samba configuration file
echo "Backing up the original Samba configuration file..."
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

# Provision Samba as an Active Directory Domain Controller
echo "Provisioning Samba as an Active Directory Domain Controller..."
samba-tool domain provision --use-rfc2307 --interactive

# Move the generated Samba configuration file to the correct location
echo "Moving the new Samba configuration file..."
cp /var/lib/samba/private/smb.conf /etc/samba/smb.conf

# Enable and start Samba services
echo "Enabling and starting Samba services..."
systemctl unmask samba-ad-dc
systemctl enable samba-ad-dc
systemctl start samba-ad-dc

# Configure SWAT (Samba Web Administration Tool)
echo "Configuring SWAT..."
sed -i 's/^disable = yes/disable = no/' /etc/xinetd.d/swat
systemctl restart xinetd

# Configure CUPS (Common Unix Printing System)
echo "Configuring CUPS..."
systemctl enable cups
systemctl start cups

# Allow SWAT and CUPS through the firewall
echo "Configuring firewall for SWAT and CUPS..."
ufw allow 901/tcp  # SWAT
ufw allow 631/tcp  # CUPS

# Display installation completion message
echo "Installation and configuration of Samba4 AD DC, SWAT, and CUPS completed!"
echo "You can access SWAT at http://$(hostname -I | awk '{print $1}'):901"
echo "You can access CUPS at http://$(hostname -I | awk '{print $1}'):631"
