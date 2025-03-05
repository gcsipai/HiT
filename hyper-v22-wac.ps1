# Define variables
$WACDownloadUrl = "https://aka.ms/WACDownload"
$WACInstallerPath = "$env:TEMP\WindowsAdminCenter.msi"
$WACPort = 443
$WACLogPath = "$env:TEMP\WACInstall.log"

# Step 1: Download Windows Admin Center
Write-Host "Downloading Windows Admin Center..."
Invoke-WebRequest -Uri $WACDownloadUrl -OutFile $WACInstallerPath

# Step 2: Install Windows Admin Center
Write-Host "Installing Windows Admin Center..."
Start-Process msiexec.exe -Wait -ArgumentList "/i $WACInstallerPath /qn /L*v $WACLogPath SME_PORT=$WACPort SSL_CERTIFICATE_OPTION=generate"

# Step 3: Configure Firewall Rules
Write-Host "Configuring Firewall Rules..."
New-NetFirewallRule -DisplayName "Windows Admin Center HTTPS" -Direction Inbound -LocalPort $WACPort -Protocol TCP -Action Allow

# Step 4: Verify Installation
Write-Host "Verifying Installation..."
$WACService = Get-Service -Name "ServerManagementGateway" -ErrorAction SilentlyContinue

if ($WACService -and $WACService.Status -eq 'Running') {
    Write-Host "Windows Admin Center installed successfully!"
    Write-Host "Access Windows Admin Center at: https://$($env:COMPUTERNAME):$WACPort"
} else {
    Write-Host "Installation failed. Check the log file at: $WACLogPath"
}

# Step 5: Cleanup (Optional)
Write-Host "Cleaning up installer..."
Remove-Item -Path $WACInstallerPath -Force
