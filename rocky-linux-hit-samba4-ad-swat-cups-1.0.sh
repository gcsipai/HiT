#!/bin/bash

# Rocky Linux HiT-Samba4-SWAT-CUPS-2025 Installation Script

# Update the system
echo "Updating system packages..."
sudo dnf update -y

# Install essential dependencies
echo "Installing dependencies..."
sudo dnf install -y epel-release
sudo dnf install -y samba samba-dc samba-client cups cockpit cockpit-samba cockpit-storaged

# Enable and start Cockpit
echo "Enabling and starting Cockpit..."
sudo systemctl enable --now cockpit.socket

# Set hostname for the AD DC (replace with your desired hostname)
echo "Setting hostname..."
sudo hostnamectl set-hostname ad-dc.example.com  # Replace with your domain

# Install Web Administration Tool (WAT)
echo "Installing Web Administration Tool (WAT)..."
sudo dnf install -y samba-web

# Configure Samba4 as an AD DC
echo "Configuring Samba4 as an Active Directory Domain Controller..."
sudo samba-tool domain provision --use-rfc2307 --interactive

# Start and enable Samba AD DC services
echo "Starting and enabling Samba AD DC services..."
sudo systemctl enable --now samba

# Configure firewall for Samba, CUPS, and Cockpit
echo "Configuring firewall..."
sudo firewall-cmd --permanent --add-service=samba
sudo firewall-cmd --permanent --add-service=cups
sudo firewall-cmd --permanent --add-service=cockpit
sudo firewall-cmd --reload

# Install and configure CUPS
echo "Installing and configuring CUPS..."
sudo systemctl enable --now cups

# Verify Samba AD DC status
echo "Verifying Samba AD DC status..."
sudo samba-tool domain level show

# Install Cockpit Samba4 module
echo "Installing Cockpit Samba4 module..."
sudo dnf install -y cockpit-samba

# Restart Cockpit to load the Samba4 module
echo "Restarting Cockpit..."
sudo systemctl restart cockpit

echo "Installation complete!"
echo "Access Cockpit at https://$(hostname -f):9090"
echo "Access Samba Web Administration Tool (WAT) at https://$(hostname -f):9090/samba"
