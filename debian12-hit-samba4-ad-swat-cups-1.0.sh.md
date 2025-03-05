Key Points in the Script
Samba4 AD DC Provisioning:

The script uses samba-tool domain provision to configure Samba as an Active Directory Domain Controller.

You will be prompted to provide details such as:

Realm: The DNS domain name (e.g., example.com).

Domain: The NetBIOS domain name (e.g., EXAMPLE).

Admin Password: The password for the Administrator account.

SWAT Configuration:

SWAT is enabled by modifying the /etc/xinetd.d/swat file.

SWAT runs on port 901 by default.

CUPS Configuration:

CUPS is installed and enabled to run on port 631.

Firewall Rules:

The script assumes ufw is installed and configures it to allow access to SWAT (port 901) and CUPS (port 631).

Post-Installation Steps
Verify Samba AD DC:

Check the status of the Samba AD DC service:

bash
Copy
sudo systemctl status samba-ad-dc
Test the domain controller functionality:

bash
Copy
sudo samba-tool domain level show
Access SWAT:

Open a web browser and navigate to http://<your-server-ip>:901.

Use the Administrator account and the password you set during provisioning to log in.

Access CUPS:

Open a web browser and navigate to http://<your-server-ip>:631.

Configure printers and manage the printing system.

Notes
DNS Configuration: Ensure that the server's DNS is correctly configured to point to itself for AD functionality.

Firewall: If you are using a different firewall (e.g., iptables), adjust the rules accordingly.

Customization: Depending on your environment, you may need to customize the Samba configuration further.

This script provides a basic setup for Samba4 AD DC, SWAT, and CUPS. You can expand it to include additional configurations as needed.

