What the Script Does
Downloads OpenVPN:

Downloads the OpenVPN installer from the official website.

Installs OpenVPN:

Installs OpenVPN silently using the MSI installer.

Configures OpenVPN Server:

Creates the configuration directory and copies sample configuration files.

Configures the OpenVPN server with a basic setup (UDP port 1194, TLS authentication, etc.).

Generates Certificates and Keys:

Uses EasyRSA to generate a Certificate Authority (CA), server certificate, Diffie-Hellman parameters, and TLS-auth key.

Sets Up OpenVPN Service:

Configures OpenVPN as a Windows service and starts it.

Configures Firewall:

Allows UDP traffic on port 1194 through the firewall.

Displays Installation Summary:

Provides the location of the configuration files and instructions for setting up VPN clients.

Notes
Client Configuration:

After installation, you need to generate client certificates and configure the client.ovpn file for VPN clients.

Use EasyRSA to generate client certificates:

powershell
Copy
.\easyrsa.bat build-client-full client1 nopass
Copy the client certificate, key, and ta.key to the client device.

Firewall Rules:

Ensure the firewall allows UDP traffic on port 1194. Adjust the script if your network requires additional rules.

OpenVPN Version:

The script downloads OpenVPN 2.6.7. Update the URL in the script if a newer version is available.

This script provides a complete setup for an OpenVPN Server on Windows Server 2022. You can customize it further based on your specific requirements.
