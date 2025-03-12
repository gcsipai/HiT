What the Script Does
Updates the system and installs essential dependencies (Python, Node.js, Docker, Nginx).

Clones the DeepSeek R1:8B repository and sets up a Python virtual environment.

Downloads the DeepSeek R1:8B model (replace the placeholder with the actual download command).

Clones the Open WebUI repository and installs its dependencies.

Configures Nginx as a reverse proxy to serve both the DeepSeek server and Open WebUI.

Creates systemd services for the DeepSeek server and Open WebUI to ensure they run on startup.

Starts and enables all services.

Accessing the Web UI
Open your browser and navigate to http://your_domain_or_ip.

Notes
Replace your_domain_or_ip with your actual domain or server IP address.

Ensure the DeepSeek R1:8B repository and model download URLs are correct.

Adjust ports and configurations as needed based on your setup.
