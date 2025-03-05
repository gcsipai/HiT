#!/bin/bash

# Debian 12 HiT-Lxc-LxcWeb-Cockpit-2025 Installation Script

# Update and upgrade the system
echo "Updating and upgrading the system..."
apt update && apt upgrade -y

# Install LXC and related tools
echo "Installing LXC and related tools..."
apt install -y lxc lxc-templates bridge-utils libvirt-clients libvirt-daemon-system

# Enable and start LXC services
echo "Enabling and starting LXC services..."
systemctl enable lxc
systemctl start lxc

# Install a web-based LXC dashboard (LXC Web Panel)
echo "Installing LXC Web Panel..."
wget https://lxc-webpanel.github.io/tools/install.sh -O - | bash

# Alternatively, install Cockpit with LXC support
# Uncomment the following lines if you prefer Cockpit over LXC Web Panel
# echo "Installing Cockpit with LXC support..."
# apt install -y cockpit cockpit-machines
# systemctl enable cockpit
# systemctl start cockpit

# Allow firewall access for the web dashboard
echo "Configuring firewall for the web dashboard..."
ufw allow 5000/tcp  # LXC Web Panel (default port)
# ufw allow 9090/tcp  # Cockpit (default port)

# Display installation completion message
echo "Installation of LXC and web dashboard completed!"
echo "You can access LXC Web Panel at http://$(hostname -I | awk '{print $1}'):5000"
# echo "You can access Cockpit at http://$(hostname -I | awk '{print $1}'):9090"
