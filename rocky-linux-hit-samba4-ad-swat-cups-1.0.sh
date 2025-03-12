#!/bin/bash

# Rocky Linux HiT-Samba4-SWAT-CUPS-2025 Installation Script
# Update the system
echo "Updating system packages..."
dnf update -y

# Install essential dependencies
echo "Installing dependencies..."
dnf install -y epel-release
dnf install -y samba samba-dc samba-client cups cockpit cockpit-samba cockpit-storaged

# Enable and start Cockpit
echo "Enabling and starting Cockpit..."
systemctl enable --now cockpit.socket

# Set hostname for the AD DC (replace with your desired hostname)
echo "Setting hostname..."
hostnamectl set-hostname ad-dc.example.com  # Replace with your domain

# Install Web Administration Tool (WAT)
echo "Installing Web Administration Tool (WAT)..."
dnf install -y samba-web

# Configure Samba4 as an AD DC
echo "Configuring Samba4 as an Active Directory Domain Controller..."
samba-tool domain provision --use-rfc2307 --interactive

# Start and enable Samba AD DC services
echo "Starting and enabling Samba AD DC services..."
systemctl enable --now samba

# Configure firewall for Samba, CUPS, and Cockpit
echo "Configuring firewall..."
firewall-cmd --permanent --add-service=samba
firewall-cmd --permanent --add-service=cups
firewall-cmd --permanent --add-service=cockpit
firewall-cmd --reload

# Install and configure CUPS
echo "Installing and configuring CUPS..."
systemctl enable --now cups

# Verify Samba AD DC status
echo "Verifying Samba AD DC status..."
samba-tool domain level show

# Install Cockpit Samba4 module
echo "Installing Cockpit Samba4 module..."
dnf install -y cockpit-samba

# Restart Cockpit to load the Samba4 module
echo "Restarting Cockpit..."
systemctl restart cockpit

echo "Installation complete!"
echo "Access Cockpit at https://$(hostname -f):9090"
echo "Access Samba Web Administration Tool (WAT) at https://$(hostname -f):9090/samba"
