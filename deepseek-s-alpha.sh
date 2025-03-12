#!/bin/bash

# Update the system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential dependencies
echo "Installing dependencies..."
sudo apt install -y curl wget git python3 python3-pip python3-venv nginx docker.io

# Install Node.js (for Open WebUI)
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# Start and enable Docker
echo "Starting Docker..."
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# Clone DeepSeek R1:8B repository (replace with actual repo URL)
echo "Cloning DeepSeek R1:8B..."
git clone https://github.com/deepseek-ai/deepseek-r1-8b.git
cd deepseek-r1-8b

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download the DeepSeek R1:8B model (replace with actual model download command)
echo "Downloading DeepSeek R1:8B model..."
# Example: wget https://example.com/deepseek-r1-8b-model.bin

# Clone Open WebUI repository
echo "Cloning Open WebUI..."
cd ~
git clone https://github.com/open-webui/open-webui.git
cd open-webui

# Install Node.js dependencies for Open WebUI
echo "Installing Node.js dependencies..."
npm install

# Build Open WebUI
echo "Building Open WebUI..."
npm run build

# Configure Nginx as a reverse proxy
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/deepseek > /dev/null <<EOL
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:3000;  # Open WebUI port
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;  # DeepSeek server port
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOL

# Enable Nginx configuration
echo "Enabling Nginx configuration..."
sudo ln -s /etc/nginx/sites-available/deepseek /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Create systemd service for DeepSeek server
echo "Creating systemd service for DeepSeek server..."
sudo tee /etc/systemd/system/deepseek-server.service > /dev/null <<EOL
[Unit]
Description=DeepSeek R1:8B Server
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)/deepseek-r1-8b
ExecStart=$(pwd)/deepseek-r1-8b/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Create systemd service for Open WebUI
echo "Creating systemd service for Open WebUI..."
sudo tee /etc/systemd/system/open-webui.service > /dev/null <<EOL
[Unit]
Description=Open WebUI
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)/open-webui
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Enable and start services
echo "Enabling and starting services..."
sudo systemctl enable deepseek-server
sudo systemctl enable open-webui
sudo systemctl start deepseek-server
sudo systemctl start open-webui

echo "Installation complete!"
echo "Access the Open WebUI at http://your_domain_or_ip"
