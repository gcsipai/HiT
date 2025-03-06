#!/bin/bash

# Update the system
echo "Updating the system..."
sudo dnf update -y

# Install required tools
echo "Installing tools: snmp, unzip, zip, htop, rar, unrar, mc, bpytop..."
sudo dnf install -y \
    net-snmp net-snmp-utils \
    unzip zip \
    htop \
    rar unrar \
    mc \
    python3-pip

# Install bpytop using pip
echo "Installing bpytop..."
sudo pip3 install bpytop

# Configure SNMP (basic setup)
echo "Configuring SNMP..."
SNMP_CONF="/etc/snmp/snmpd.conf"
sudo cp $SNMP_CONF $SNMP_CONF.bak  # Backup the original config

# Add basic SNMP configuration
sudo cat <<EOF | sudo tee $SNMP_CONF > /dev/null
com2sec readonly  default       public
group   MyROGroup v2c           readonly
view    all       included   .1
access  MyROGroup ""      any       noauth    exact  all    none   none
syslocation "My Location"
syscontact My Contact <myemail@example.com>
EOF

# Enable and start SNMP service
echo "Enabling and starting SNMP service..."
sudo systemctl enable snmpd
sudo systemctl start snmpd

# Verify SNMP service status
echo "Checking SNMP service status..."
sudo systemctl status snmpd

# Verify installed tools
echo "Verifying installed tools..."
for tool in snmpd unzip zip htop rar unrar mc bpytop; do
    if command -v $tool &> /dev/null; then
        echo "$tool is installed."
    else
        echo "$tool is NOT installed."
    fi
done

echo "Installation and configuration completed!"
