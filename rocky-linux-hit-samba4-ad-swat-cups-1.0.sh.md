What the Script Does
Updates the system and installs essential dependencies.

Installs Samba4 AD DC, CUPS, Cockpit, and the Cockpit Samba4 module.

Sets the hostname for the AD DC (replace ad-dc.example.com with your desired hostname).

Configures Samba4 as an Active Directory Domain Controller interactively.

Enables and starts Samba, CUPS, and Cockpit services.

Configures the firewall to allow Samba, CUPS, and Cockpit traffic.

Installs the Web Administration Tool (WAT) for Samba.

Verifies the Samba AD DC status.

Restarts Cockpit to load the Samba4 module.

Accessing the Services
Cockpit: Access at https://<your-server-ip>:9090.

Samba Web Administration Tool (WAT): Access at https://<your-server-ip>:9090/samba.

CUPS: Access at http://<your-server-ip>:631.

Notes
Replace ad-dc.example.com with your desired domain name during the Samba4 AD DC configuration.

Ensure your system meets the requirements for running an AD DC (e.g., sufficient RAM, CPU, and disk space).

You can customize the Samba4 AD DC configuration by editing the /etc/samba/smb.conf file after installation.
