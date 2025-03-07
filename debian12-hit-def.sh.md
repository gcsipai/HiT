What the Script Does:
Updates the package list to ensure the latest versions of packages are available.

Installs the specified packages:

mc: Midnight Commander (file manager).

htop: Interactive process viewer.

unzip, zip: Tools for handling ZIP archives.

unrar, rar: Tools for handling RAR archives.

bpytop: Resource monitor (Python-based).

snmp, snmpd, snmp-mibs-downloader: SNMP tools and daemon.

Configures SNMP:

Backs up the original snmpd.conf file.

Sets up a basic SNMPv2 configuration with the community string public.

Configures system information, disk, and process monitoring.

Enables and starts the SNMP service:

Restarts the snmpd service to apply the new configuration.

Ensures the SNMP service starts automatically at boot.

Checks if the SNMP service is running and provides feedback.

Notes:
SNMP Community String: The community string is set to public in this script. For security reasons, you should change this to a custom string in the /etc/snmp/snmpd.conf file after running the script.

Firewall: Ensure UDP port 161 is open if you want to allow SNMP queries from remote systems.

SNMPv3: If you need SNMPv3 (more secure), additional configuration is required (e.g., creating users and enabling encryption). Let me know if you need help with this.
