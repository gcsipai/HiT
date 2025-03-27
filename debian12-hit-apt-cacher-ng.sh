!/bin/bash
# APT Cache és Windows Update Szerver HiT Beállító Script

# Root jog ellenőrzése
if [ "$(id -u)" -ne 0 ]; then
  echo "A script root jogosultsággal kell futnia!" >&2
  exit 1
fi

# 1. Rendszer frissítése
echo "### Rendszer frissítése ###"
apt update && apt upgrade -y

# 2. APT Cache (apt-cacher-ng) telepítése
echo "### APT Cache telepítése ###"
apt install -y apt-cacher-ng

# 3. APT Cache konfigurálása
echo "### Konfiguráció beállítása ###"
cat > /etc/apt-cacher-ng/acng.conf <<EOL
# Alapkonfiguráció
CacheDir: /var/cache/apt-cacher-ng
LogDir: /var/log/apt-cacher-ng
Port: 3142
BindAddress: 0.0.0.0

# Windows Update cache beállítások
Remap-win: http://windowsupdate.microsoft.com http://wsus.domain.local:8530
Remap-win: http://*.windowsupdate.microsoft.com http://wsus.domain.local:8530
Remap-win: http://*.update.microsoft.com http://wsus.domain.local:8530
EOL

# 4. Szolgáltatás újraindítása
systemctl restart apt-cacher-ng

