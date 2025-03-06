What the Script Does:
Updates the System: Ensures the system is up-to-date.

Installs Required Tools:

snmp: Simple Network Management Protocol tools.

unzip, zip: Tools for handling ZIP archives.

htop: Interactive process viewer.

rar, unrar: Tools for handling RAR archives.

mc: Midnight Commander, a terminal-based file manager.

bpytop: A resource monitor for the terminal (installed via pip3).

Configures SNMP:

Backs up the original SNMP configuration file.

Sets up a basic SNMP configuration with the community string public.

Enables and starts the SNMP service.

Verifies Installation: Checks if all tools are installed correctly.

Post-Installation:
SNMP Configuration: You can further customize the SNMP configuration in /etc/snmp/snmpd.conf if needed.

bpytop: Run bpytop in the terminal to see system resource usage.

Midnight Commander: Run mc in the terminal to use the file manager.

Notes:
SNMP Community String: The default community string is set to public. For production environments, change this to a more secure value.

bpytop: If you encounter issues with bpytop, ensure that python3 and pip3 are installed correctly.

This script should work on Rocky Linux 8 and 9. Adjustments may be needed for other distributions or specific use cases.
