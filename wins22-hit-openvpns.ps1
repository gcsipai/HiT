# Define variables
$openvpnUrl = "https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.7-I001-amd64.msi"
$installerPath = "$env:TEMP\OpenVPN-Installer.msi"
$openvpnDir = "C:\Program Files\OpenVPN"
$configDir = "$openvpnDir\config"
$easyrsaDir = "$openvpnDir\easy-rsa"

# Download OpenVPN installer
Write-Host "Downloading OpenVPN installer..."
Invoke-WebRequest -Uri $openvpnUrl -OutFile $installerPath

# Install OpenVPN silently
Write-Host "Installing OpenVPN..."
Start-Process -FilePath msiexec.exe -ArgumentList "/i `"$installerPath`" /quiet /norestart" -Wait

# Clean up installer
Write-Host "Cleaning up installer..."
Remove-Item -Path $installerPath -Force

# Create OpenVPN config directory
Write-Host "Creating OpenVPN config directory..."
New-Item -ItemType Directory -Path $configDir -Force

# Copy sample configuration files
Write-Host "Copying sample configuration files..."
Copy-Item -Path "$openvpnDir\sample-config\server.ovpn" -Destination "$configDir\server.conf"
Copy-Item -Path "$openvpnDir\sample-config\client.ovpn" -Destination "$configDir\client.ovpn"

# Configure OpenVPN server
Write-Host "Configuring OpenVPN server..."
$serverConfig = @"
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "route 192.168.1.0 255.255.255.0"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
keepalive 10 120
tls-auth ta.key 0
cipher AES-256-CBC
persist-key
persist-tun
status openvpn-status.log
verb 3
"@
Set-Content -Path "$configDir\server.conf" -Value $serverConfig

# Generate certificates and keys using EasyRSA
Write-Host "Setting up EasyRSA for certificate generation..."
Copy-Item -Path "$openvpnDir\easy-rsa" -Destination $easyrsaDir -Recurse -Force
Set-Location -Path $easyrsaDir

# Initialize PKI
Write-Host "Initializing PKI..."
.\easyrsa-init.bat
.\easyrsa.bat --batch init-pki

# Build CA
Write-Host "Building CA..."
.\easyrsa.bat --batch build-ca nopass

# Generate server certificate
Write-Host "Generating server certificate..."
.\easyrsa.bat --batch build-server-full server nopass

# Generate Diffie-Hellman parameters
Write-Host "Generating Diffie-Hellman parameters..."
.\easyrsa.bat gen-dh

# Generate TLS-auth key
Write-Host "Generating TLS-auth key..."
openvpn --genkey --secret "$configDir\ta.key"

# Copy certificates and keys to config directory
Write-Host "Copying certificates and keys to config directory..."
Copy-Item -Path "$easyrsaDir\pki\ca.crt" -Destination $configDir
Copy-Item -Path "$easyrsaDir\pki\issued\server.crt" -Destination $configDir
Copy-Item -Path "$easyrsaDir\pki\private\server.key" -Destination $configDir
Copy-Item -Path "$easyrsaDir\pki\dh.pem" -Destination $configDir

# Configure OpenVPN service
Write-Host "Configuring OpenVPN service..."
New-Service -Name "OpenVPNService" -BinaryPathName "`"$openvpnDir\bin\openvpn.exe`" --service --config `"$configDir\server.conf`"" -DisplayName "OpenVPN Server" -StartupType Automatic

# Start OpenVPN service
Write-Host "Starting OpenVPN service..."
Start-Service -Name "OpenVPNService"

# Allow OpenVPN through the firewall
Write-Host "Allowing OpenVPN through the firewall..."
New-NetFirewallRule -DisplayName "OpenVPN" -Direction Inbound -Protocol UDP -LocalPort 1194 -Action Allow

# Display installation summary
Write-Host "OpenVPN Server installation complete!"
Write-Host "OpenVPN configuration directory: $configDir"
Write-Host "Client configuration template: $configDir\client.ovpn"
Write-Host "Generate client certificates and configure the client.ovpn file for VPN clients."
