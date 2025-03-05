Explanation of the Script
Download Windows Admin Center:

The script downloads the Windows Admin Center installer from the official Microsoft URL (https://aka.ms/WACDownload) and saves it to the %TEMP% folder.

Install Windows Admin Center:

The installer runs in quiet mode (/qn) to avoid user interaction.

The SME_PORT parameter specifies the port (default is 443) on which Windows Admin Center will run.

The SSL_CERTIFICATE_OPTION=generate parameter generates a self-signed SSL certificate for HTTPS.

Configure Firewall Rules:

A new firewall rule is created to allow inbound traffic on the specified port (default is 443).

Verify Installation:

The script checks if the ServerManagementGateway service is running to confirm a successful installation.

If the service is running, it provides the URL to access Windows Admin Center.

Cleanup:

The installer file is deleted to free up space.

How to Use the Script
Copy the script into a .ps1 file, e.g., Install-WAC.ps1.

Run the script on your Windows Hyper-V Server 2022 instance with elevated privileges (Run as Administrator):

powershell
Copy
.\Install-WAC.ps1
After the script completes, open a web browser and navigate to:

Copy
https://<YourServerIP>:443
Replace <YourServerIP> with the IP address or hostname of your server.

Log in using your Windows credentials.

Notes
Self-Signed Certificate: The script generates a self-signed certificate. For production environments, consider using a trusted certificate.

Firewall Configuration: Ensure the firewall allows inbound traffic on the specified port (default is 443).

Logs: If the installation fails, check the log file at %TEMP%\WACInstall.log for details.

This script provides a fully automated way to install and configure Windows Admin Center on Windows Hyper-V Server 2022.
