#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt update

# Install the required packages
echo "Installing packages..."
sudo apt install -y mc htop unzip zip unrar rar bpytop snmp snmpd snmp-mibs-downloader

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "All packages installed successfully!"
else
    echo "Failed to install some packages. Please check the output above."
    exit 1
fi

# Backup the original SNMP configuration file
echo "Backing up the original SNMP configuration file..."
sudo cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.bak

# Configure SNMP (SNMPv2 with community string 'public')
echo "Configuring SNMP (SNMPv2 with community string 'public')..."
sudo bash -c 'cat > /etc/snmp/snmpd.conf << EOF
# Listen on all interfaces
agentAddress udp:161

# SNMPv2 community string (set to "public")
rocommunity public

# System information
sysLocation  "Your Location"
sysContact  "Your Contact Info"
sysName  $(hostname)

# Include disk and process monitoring
includeAllDisks  10%
includeAllProcesses

# Enable logging
trap2sink localhost
EOF'

# Restart and enable SNMP service
echo "Restarting and enabling SNMP service..."
sudo systemctl restart snmpd
sudo systemctl enable snmpd

# Check if SNMP service is running
if systemctl is-active --quiet snmpd; then
    echo "SNMP service is running successfully!"
else
    echo "Failed to start SNMP service. Please check the configuration."
    exit 1
fi

echo "Installation and configuration completed successfully!"
