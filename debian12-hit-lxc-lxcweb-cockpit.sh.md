Instructions to Use the Script
Save the Script: Save the script to a file, e.g., install_lxc_web_dashboard.sh.

Make the Script Executable: Run the following command to make the script executable:

bash
Copy
chmod +x install_lxc_web_dashboard.sh
Run the Script: Execute the script with root privileges:

bash
Copy
sudo ./install_lxc_web_dashboard.sh
Key Points in the Script
LXC Installation:

Installs LXC, LXC templates, and related tools (bridge-utils, libvirt-clients, libvirt-daemon-system).

Enables and starts the LXC service.

Web Dashboard Installation:

LXC Web Panel: A lightweight web-based dashboard for managing LXC containers. It runs on port 5000 by default.

Cockpit: A more advanced web-based management tool with LXC support. It runs on port 9090 by default. Uncomment the relevant lines in the script if you prefer Cockpit.

Firewall Configuration:

The script configures ufw to allow access to the web dashboard (port 5000 for LXC Web Panel or port 9090 for Cockpit).

Post-Installation Steps
Access LXC Web Panel:

Open a web browser and navigate to http://<your-server-ip>:5000.

The default login credentials for LXC Web Panel are:

Username: admin

Password: admin

Access Cockpit (if installed):

Open a web browser and navigate to http://<your-server-ip>:9090.

Log in with your system credentials.

Create and Manage Containers:

Use the web dashboard to create, start, stop, and manage LXC containers.

Notes
LXC Web Panel: This is a simple and lightweight dashboard for managing LXC containers. It is easy to set up but may lack advanced features.

Cockpit: Cockpit is a more powerful tool that supports not only LXC but also virtual machines, storage, networking, and more. It is recommended for users who need a comprehensive management interface.

Firewall: If you are using a different firewall (e.g., iptables), adjust the rules accordingly.

Security: Change the default credentials for LXC Web Panel after the first login.

This script provides a basic setup for LXC and a web dashboard. You can expand it to include additional configurations as needed.
