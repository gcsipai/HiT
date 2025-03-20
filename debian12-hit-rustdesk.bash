#!/bin/bash

# Frissítés és szükséges csomagok telepítése
sudo apt update
sudo apt upgrade -y
sudo apt install -y curl wget unzip

# RustDesk szerver letöltése
RUSTDESK_VERSION="1.1.9"
wget https://github.com/rustdesk/rustdesk-server/releases/download/${RUSTDESK_VERSION}/rustdesk-server-linux-x64.zip

# Kicsomagolás
unzip rustdesk-server-linux-x64.zip -d rustdesk-server

# Mappa létrehozása és fájlok áthelyezése
sudo mkdir -p /opt/rustdesk-server
sudo mv rustdesk-server/* /opt/rustdesk-server/

# Szükséges jogosultságok beállítása
sudo chmod +x /opt/rustdesk-server/hbbs
sudo chmod +x /opt/rustdesk-server/hbbr

# Systemd szolgáltatás létrehozása a hbbs-hez
sudo bash -c 'cat > /etc/systemd/system/rustdesk-hbbs.service <<EOF
[Unit]
Description=RustDesk HBBS Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/rustdesk-server/hbbs
WorkingDirectory=/opt/rustdesk-server
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF'

# Systemd szolgáltatás létrehozása a hbbr-hez
sudo bash -c 'cat > /etc/systemd/system/rustdesk-hbbr.service <<EOF
[Unit]
Description=RustDesk HBBR Server
After=network.target

[Service]
Type=simple
ExecStart=/opt/rustdesk-server/hbbr
WorkingDirectory=/opt/rustdesk-server
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF'

# Szolgáltatások indítása és engedélyezése
sudo systemctl daemon-reload
sudo systemctl start rustdesk-hbbs
sudo systemctl enable rustdesk-hbbs
sudo systemctl start rustdesk-hbbr
sudo systemctl enable rustdesk-hbbr

# Tűzfal beállítása (ha szükséges)
sudo ufw allow 21115:21119/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 21116/udp

echo "RustDesk szerver telepítése befejeződött!"
echo "A hbbs fut a 21115-es porton, a hbbr pedig a 21116-os porton."
