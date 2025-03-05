What the Script Does
Updates the System:

Ensures the system is up-to-date.

Installs Required Packages:

Installs Samba, SWAT, CUPS, Samba Terminal GUI, and Nextcloud.

Configures Samba as an AD DC:

Uses samba-tool to provision Samba as an Active Directory Domain Controller.

Configures SWAT:

Enables SWAT for web-based Samba administration.

Configures CUPS:

Sets up CUPS for printing services.

Installs Samba Terminal GUI:

Provides a graphical interface for Samba management.

Installs Nextcloud:

Sets up Nextcloud for file sharing and collaboration.

Restarts Services:

Ensures all services are running.

Post-Installation Steps
Access SWAT:

Open a browser and go to http://your-server-ip:901.

Access Nextcloud:

Open a browser and go to http://your-server-ip/nextcloud.

Configure Samba AD DC:

Use samba-tool or SWAT to manage users, groups, and shares.

Configure CUPS:

Access CUPS at http://your-server-ip:631 to set up printers.

Notes
Replace your-server-ip with the actual IP address of your server.

Ensure you have a static IP address configured on your server.

Customize the domain and other settings during the Samba AD DC provisioning step.

Test the script in a lab environment before deploying it in production.

Let me know if you need further assistance!
