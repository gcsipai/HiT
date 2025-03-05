What the Script Does
Updates the System:

Updates and upgrades the system packages.

Installs Apache2:

Installs the Apache2 web server and enables it to start on boot.

Installs PHP 8.2:

Installs PHP 8.2 and common PHP modules required for web development.

Installs MariaDB:

Installs the MariaDB database server and secures it with a root password.

Creates a Test Database:

Creates a test database (testdb) and a user (testuser) with full privileges.

Installs phpMyAdmin:

Installs phpMyAdmin, a web-based database management tool, and configures it to work with Apache2.

Installs Cockpit and Cockpit Apache2 Module:

Installs Cockpit, a web-based server management tool, and its Apache2 module for managing Apache2 via Cockpit.

Enables and Starts Cockpit:

Enables and starts the Cockpit service, making it accessible via a web browser.

Restarts Apache2:

Restarts Apache2 to apply all changes.

Displays Installation Summary:

Provides URLs and credentials for accessing the installed services.

Accessing the Services
Apache2: Open your browser and navigate to http://localhost/.

phpMyAdmin: Open your browser and navigate to http://localhost/phpmyadmin/.

Use the following credentials to log in:

Username: testuser

Password: testpassword

Cockpit: Open your browser and navigate to https://localhost:9090/.

Use your system credentials to log in.

Notes
MariaDB Root Password: The script sets the MariaDB root password to password. Change this to a secure password in production environments.

Test Database: The script creates a test database and user for demonstration purposes. Remove or modify this section if not needed.

Cockpit: Cockpit is a powerful web-based tool for server management. Ensure you secure it with a strong password and restrict access to trusted IPs.

Cockpit Apache2 Module: This module allows you to manage Apache2 directly from the Cockpit interface.

This script provides a quick and automated way to set up a LAMP stack with phpMyAdmin and Cockpit on Debian 12 for web development and server management.
