import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import socket
import time
import threading

# Számítógépnév lekérése
def get_computer_name():
    return socket.gethostname()

# Folyamatcsík frissítése
def update_progress(value):
    progress['value'] = value
    root.update_idletasks()

# Hostname (számítógépnév) változtatása
def change_hostname():
    new_hostname = hostname_entry.get()
    if not new_hostname:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy számítógénevet!")
        return

    def change():
        try:
            update_progress(20)
            # Számítógépnév változtatása PowerShell paranccsal
            command = f"Rename-Computer -NewName {new_hostname} -Force"
            subprocess.run(["powershell", "-Command", command], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", f"A számítógépnév sikeresen megváltoztatva erre: {new_hostname}")
            computer_name_label.config(text=f"Aktuális számítógépnév: {new_hostname}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a számítógépnév változtatása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=change).start()

# IPv6 be- és kikapcsolása
def toggle_ipv6():
    def toggle():
        try:
            update_progress(20)
            # IPv6 állapotának lekérése
            result = subprocess.run(
                ["powershell", "Get-NetAdapterBinding -ComponentID ms_tcpip6"],
                capture_output=True, text=True
            )
            if "Enabled" in result.stdout:
                # IPv6 kikapcsolása
                subprocess.run(["powershell", "Disable-NetAdapterBinding -ComponentID ms_tcpip6 -Name *"], check=True)
                update_progress(100)
                messagebox.showinfo("Siker", "IPv6 sikeresen kikapcsolva.")
            else:
                # IPv6 bekapcsolása
                subprocess.run(["powershell", "Enable-NetAdapterBinding -ComponentID ms_tcpip6 -Name *"], check=True)
                update_progress(100)
                messagebox.showinfo("Siker", "IPv6 sikeresen bekapcsolva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt az IPv6 állapotának változtatása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=toggle).start()

# Idő szinkronizálása magyarországi szerverrel
def sync_time():
    def sync():
        try:
            update_progress(20)
            # Időszinkronizációs szerver beállítása (Budapesti szerver)
            subprocess.run(["powershell", "Start-Process w32tm -ArgumentList '/config /syncfromflags:manual /manualpeerlist:ntp.iif.hu' -Verb RunAs"], check=True)
            update_progress(50)
            # Szolgáltatás újraindítása
            subprocess.run(["powershell", "Start-Process w32tm -ArgumentList '/resync' -Verb RunAs"], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", "Az idő sikeresen szinkronizálva a magyarországi szerverrel.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt az idő szinkronizálása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=sync).start()

# SNMP szolgáltatás telepítése és bekapcsolása
def install_snmp():
    def install():
        try:
            update_progress(20)
            # SNMP szolgáltatás telepítése
            subprocess.run(["powershell", "Add-WindowsCapability -Online -Name SNMP.Client~~~~0.0.1.0"], check=True)
            update_progress(50)
            # SNMP szolgáltatás bekapcsolása
            subprocess.run(["powershell", "Set-Service -Name SNMP -StartupType Automatic"], check=True)
            subprocess.run(["powershell", "Start-Service -Name SNMP"], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", "Az SNMP szolgáltatás sikeresen telepítve és bekapcsolva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt az SNMP szolgáltatás telepítése közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=install).start()

# BitLocker kikapcsolása
def disable_bitlocker():
    def disable():
        try:
            update_progress(20)
            # BitLocker kikapcsolása PowerShell paranccsal
            subprocess.run(["powershell", "Disable-BitLocker -MountPoint C:"], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", "A BitLocker sikeresen kikapcsolva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a BitLocker kikapcsolása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=disable).start()

# Felhasználó hozzáadása
def add_user():
    username = user_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy felhasználónevet és jelszót!")
        return

    def add():
        try:
            update_progress(20)
            # Felhasználó hozzáadása PowerShell paranccsal
            command = f'New-LocalUser -Name "{username}" -Password (ConvertTo-SecureString "{password}" -AsPlainText -Force)'
            subprocess.run(["powershell", "-Command", command], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", f"A felhasználó '{username}' sikeresen hozzáadva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a felhasználó hozzáadása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=add).start()

# SMBv1 protokoll bekapcsolása
def enable_smbv1():
    def enable():
        try:
            update_progress(20)
            # SMBv1 protokoll bekapcsolása PowerShell paranccsal
            subprocess.run(["powershell", "Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol"], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", "Az SMBv1 protokoll sikeresen bekapcsolva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt az SMBv1 protokoll bekapcsolása közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=enable).start()

# Tartományhoz csatlakozás
def join_domain():
    domain = simpledialog.askstring("Tartományhoz csatlakozás", "Add meg a tartománynevet (pl. example.com):")
    if not domain:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy tartománynevet!")
        return

    username = simpledialog.askstring("Tartományhoz csatlakozás", "Add meg a tartományi adminisztrátor felhasználónevet:")
    if not username:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy felhasználónevet!")
        return

    password = simpledialog.askstring("Tartományhoz csatlakozás", "Add meg a tartományi adminisztrátor jelszavát:", show="*")
    if not password:
        messagebox.showwarning("Figyelem", "Kérlek adj meg egy jelszót!")
        return

    def join():
        try:
            update_progress(20)
            # Tartományhoz csatlakozás PowerShell paranccsal
            command = f'Add-Computer -DomainName "{domain}" -Credential (New-Object System.Management.Automation.PSCredential("{username}", (ConvertTo-SecureString "{password}" -AsPlainText -Force))) -Restart'
            subprocess.run(["powershell", "-Command", command], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", f"A számítógép sikeresen csatlakozott a(z) '{domain}' tartományhoz.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a tartományhoz csatlakozás közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=join).start()

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

# Felhasználó hozzáadása
user_label = tk.Label(root, text="Felhasználónév:")
user_label.pack(pady=5)

user_entry = tk.Entry(root)
user_entry.pack(pady=5)

password_label = tk.Label(root, text="Jelszó:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

add_user_button = tk.Button(root, text="Felhasználó hozzáadása", command=add_user)
add_user_button.pack(pady=10)

# SMBv1 protokoll bekapcsolása
smbv1_button = tk.Button(root, text="SMBv1 protokoll bekapcsolása", command=enable_smbv1)
smbv1_button.pack(pady=10)

# Tartományhoz csatlakozás
domain_button = tk.Button(root, text="Tartományhoz csatlakozás", command=join_domain)
domain_button.pack(pady=10)

# Folyamatcsík
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

# Főciklus indítása
root.mainloop()
