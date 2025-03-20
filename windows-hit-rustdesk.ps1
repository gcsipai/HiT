# RustDesk kliens letöltése
$rustdeskUrl = "https://github.com/rustdesk/rustdesk/releases/download/1.1.9/rustdesk-1.1.9-windows_x64.zip"
$outputPath = "$env:TEMP\rustdesk.zip"
Invoke-WebRequest -Uri $rustdeskUrl -OutFile $outputPath

# Kicsomagolás
$extractPath = "$env:TEMP\rustdesk"
Expand-Archive -Path $outputPath -DestinationPath $extractPath -Force

# RustDesk indítása
Start-Process "$extractPath\rustdesk.exe"

# Törlés a letöltött zip fájlból
Remove-Item -Path $outputPath -Force

Write-Host "RustDesk kliens telepítése befejeződött!"
