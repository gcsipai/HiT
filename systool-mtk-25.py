import tkinter as tk
from tkinter import messagebox
import subprocess
import socket

# Számítógépnév lekérése
def get_computer_name():
    return socket.gethostname()

# Hostname (számítógépnév) változtatása
def change_hostname():
    new_hostname = hostname_entry.get()
    if not new_hostname:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy számítógénevet!")
        return

    try:
        # Számítógépnév változtatása PowerShell paranccsal
        command = f"Rename-Computer -NewName {new_hostname} -Force"
        subprocess.run(["powershell", "-Command", command], check=True)
        messagebox.showinfo("Siker", f"A számítógépnév sikeresen megváltoztatva erre: {new_hostname}")
        computer_name_label.config(text=f"Aktuális számítógépnév: {new_hostname}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a számítógépnév változtatása közben: {e}")

# IPv6 be- és kikapcsolása
def toggle_ipv6():
    try:
        # IPv6 állapotának lekérése
        result = subprocess.run(
            ["powershell", "Get-NetAdapterBinding -ComponentID ms_tcpip6"],
            capture_output=True, text=True
        )
        if "Enabled" in result.stdout:
            # IPv6 kikapcsolása
            subprocess.run(["powershell", "Disable-NetAdapterBinding -ComponentID ms_tcpip6 -Name *"], check=True)
            messagebox.showinfo("Siker", "IPv6 sikeresen kikapcsolva.")
        else:
            # IPv6 bekapcsolása
            subprocess.run(["powershell", "Enable-NetAdapterBinding -ComponentID ms_tcpip6 -Name *"], check=True)
            messagebox.showinfo("Siker", "IPv6 sikeresen bekapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt az IPv6 állapotának változtatása közben: {e}")

# Idő szinkronizálása magyarországi szerverrel
def sync_time():
    try:
        # Időszinkronizációs szerver beállítása (Budapesti szerver)
        subprocess.run(["powershell", "w32tm /config /syncfromflags:manual /manualpeerlist:ntp.iif.hu"], check=True)
        # Szolgáltatás újraindítása
        subprocess.run(["powershell", "w32tm /resync"], check=True)
        messagebox.showinfo("Siker", "Az idő sikeresen szinkronizálva a magyarországi szerverrel.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt az idő szinkronizálása közben: {e}")

# SNMP szolgáltatás telepítése és bekapcsolása
def install_snmp():
    try:
        # SNMP szolgáltatás telepítése
        subprocess.run(["powershell", "Install-WindowsFeature -Name SNMP-Service"], check=True)
        # SNMP szolgáltatás bekapcsolása
        subprocess.run(["powershell", "Set-Service -Name SNMP -StartupType Automatic"], check=True)
        subprocess.run(["powershell", "Start-Service -Name SNMP"], check=True)
        messagebox.showinfo("Siker", "Az SNMP szolgáltatás sikeresen telepítve és bekapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt az SNMP szolgáltatás telepítése közben: {e}")

# BitLocker kikapcsolása
def disable_bitlocker():
    try:
        # BitLocker kikapcsolása PowerShell paranccsal
        subprocess.run(["powershell", "Disable-BitLocker -MountPoint C:"], check=True)
        messagebox.showinfo("Siker", "A BitLocker sikeresen kikapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a BitLocker kikapcsolása közben: {e}")

# Grafikus felület létrehozása
root = tk.Tk()
root.title("Rendszer Beállítások")

# Számítógépnév megjelenítése
computer_name = get_computer_name()
computer_name_label = tk.Label(root, text=f"Aktuális számítógépnév: {computer_name}")
computer_name_label.pack(pady=10)

# Számítógépnév változtatása
hostname_label = tk.Label(root, text="Új számítógépnév:")
hostname_label.pack(pady=5)

hostname_entry = tk.Entry(root)
hostname_entry.pack(pady=5)

hostname_button = tk.Button(root, text="Számítógépnév változtatása", command=change_hostname)
hostname_button.pack(pady=10)

# IPv6 be- és kikapcsolása
ipv6_button = tk.Button(root, text="IPv6 be/kikapcsolása", command=toggle_ipv6)
ipv6_button.pack(pady=10)

# Idő szinkronizálása magyarországi szerverrel
time_sync_button = tk.Button(root, text="Idő szinkronizálása (Magyarország)", command=sync_time)
time_sync_button.pack(pady=10)

# SNMP szolgáltatás telepítése és bekapcsolása
snmp_button = tk.Button(root, text="SNMP telepítése és bekapcsolása", command=install_snmp)
snmp_button.pack(pady=10)

# BitLocker kikapcsolása
bitlocker_button = tk.Button(root, text="BitLocker kikapcsolása", command=disable_bitlocker)
bitlocker_button.pack(pady=10)

# Főciklus indítása
root.mainloop()
