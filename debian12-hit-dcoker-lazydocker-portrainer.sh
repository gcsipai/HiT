#!/bin/bash

# Debian 12 HiT-Docker-LayzDocker-Portrainer Installation Script

# Update and upgrade the system
apt update && apt upgrade -y

# Install required dependencies
apt install -y curl apt-transport-https ca-certificates software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list and install Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker service
systemctl enable --now docker

# Add the current user to the Docker group to avoid using with Docker commands
usermod -aG docker $USER

# Install Lazydocker
LAZYDOCKER_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazydocker/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')
curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/download/${LAZYDOCKER_VERSION}/lazydocker_${LAZYDOCKER_VERSION}_Linux_x86_64.tar.gz"
tar xf lazydocker.tar.gz lazydocker
mv lazydocker /usr/local/bin/
rm lazydocker.tar.gz

# Install Portainer
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

# Print installation details
echo "Docker, Lazydocker, and Portainer have been installed successfully!"
echo "To use Docker without, log out and log back in."
echo "Access Portainer at http://localhost:9000"
echo "Run Lazydocker by typing 'lazydocker' in the terminal."
