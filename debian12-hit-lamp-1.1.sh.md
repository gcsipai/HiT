Instructions:
Save the script to a file, e.g., install_stack.sh.

Make the script executable:

bash
Copy
chmod +x install_stack.sh
Run the script:

bash
Copy
./install_stack.sh
What the Script Does:
Updates the system and installs required packages.

Installs Apache2 as the web server.

Installs MariaDB as the database server and secures it.

Installs PHP 8 and necessary modules.

Installs phpMyAdmin and configures it to work with Apache.

Downloads and installs Apache2 Admin (a web-based Apache configuration tool).

Sets permissions for Apache2 Admin and enables necessary Apache modules.

Prints instructions for accessing the installed services.

Notes:
Replace your_password in the MariaDB secure installation section with your desired root password.

After installation, you can access:

phpMyAdmin: http://localhost/phpmyadmin

Apache2 Admin: http://localhost/apache2-admin

Ensure you secure the Apache2 Admin interface, as it provides access to Apache configuration files.

Let me know if you need further assistance!
