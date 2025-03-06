Explanation of the Script:
System Update:

Updates and upgrades the system to ensure all packages are up to date.

Dependencies:

Installs required packages for FOG, including Apache, PHP, MariaDB, TFTP, NFS, and FTP.

FOG Installation:

Downloads and installs FOG from the official GitHub repository.

Runs the FOG installer (installfog.sh), which will prompt for configuration options during installation.

Apache Configuration:

Enables the FOG Apache configuration and the rewrite module.

Restarts Apache to apply changes.

NFS Configuration:

Configures NFS for FOG image storage.

Restarts the NFS service.

TFTP Configuration:

Updates the TFTP directory to /tftpboot (required by FOG).

Restarts the TFTP service.

FTP Configuration:

Enables local access and write permissions in the FTP configuration.

Restarts the FTP service.

MariaDB Configuration:

Creates a database and user for FOG.

Grants necessary privileges to the FOG user.

Service Restart:

Restarts all relevant services to apply configuration changes.

Finalize Installation:

Runs the FOG installer again to finalize the installation.

Notes:
FOG DHCP Server: The script skips the FOG DHCP server installation. Ensure you have a working DHCP server (e.g., ISC DHCP or another DHCP server) configured to work with FOG.

Database Password: Replace fogpassword with a secure password for the FOG database user.

Web Interface: After installation, access the FOG web interface at http://your-server-ip/fog.

TFTP Directory: Ensure the TFTP directory (/tftpboot) exists and has the correct permissions.

