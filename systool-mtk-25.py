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
            result = subprocess.run(
                ["powershell", "Get-NetAdapterBinding -ComponentID ms_tcpip6"],
                capture_output=True, text=True
            )
            if "Enabled" in result.stdout:
                subprocess.run(["powershell", "Disable-NetAdapterBinding -ComponentID ms_tcpip6 -Name *"], check=True)
                update_progress(100)
                messagebox.showinfo("Siker", "IPv6 sikeresen kikapcsolva.")
            else:
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
            subprocess.run(["powershell", "Start-Process w32tm -ArgumentList '/config /syncfromflags:manual /manualpeerlist:ntp.iif.hu' -Verb RunAs"], check=True)
            update_progress(50)
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
            subprocess.run(["powershell", "Add-WindowsCapability -Online -Name SNMP.Client~~~~0.0.1.0"], check=True)
            update_progress(50)
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
            command = f'Add-Computer -DomainName "{domain}" -Credential (New-Object System.Management.Automation.PSCredential("{username}", (ConvertTo-SecureString "{password}" -AsPlainText -Force))) -Restart'
            subprocess.run(["powershell", "-Command", command], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", f"A számítógép sikeresen csatlakozott a(z) '{domain}' tartományhoz.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a tartományhoz csatlakozás közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=join).start()

# Rendszerinformációk lekérése
def get_system_info():
    try:
        cpu_info = subprocess.run(["powershell", "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name"], capture_output=True, text=True)
        memory_info = subprocess.run(["powershell", "Get-WmiObject Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object -ExpandProperty Sum"], capture_output=True, text=True)
        messagebox.showinfo("Rendszerinformációk", f"CPU: {cpu_info.stdout}\nMemória: {int(memory_info.stdout) / 1024 / 1024 / 1024:.2f} GB")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a rendszerinformációk lekérése közben: {e}")

# Tűzfal bekapcsolása
def enable_firewall():
    try:
        subprocess.run(["powershell", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"], check=True)
        messagebox.showinfo("Siker", "A tűzfal sikeresen bekapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a tűzfal bekapcsolása közben: {e}")

# Tűzfal kikapcsolása
def disable_firewall():
    try:
        subprocess.run(["powershell", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"], check=True)
        messagebox.showinfo("Siker", "A tűzfal sikeresen kikapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a tűzfal kikapcsolása közben: {e}")

# Távoli asztal bekapcsolása
def enable_remote_desktop():
    try:
        subprocess.run(["powershell", "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 0"], check=True)
        subprocess.run(["powershell", "Enable-NetFirewallRule -DisplayGroup 'Távoli asztal'"], check=True)
        messagebox.showinfo("Siker", "A távoli asztal sikeresen bekapcsolva.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hiba", f"Hiba történt a távoli asztal bekapcsolása közben: {e}")

# Windows Update keresése és telepítése
def run_windows_update():
    def update():
        try:
            update_progress(20)
            subprocess.run(["powershell", "Start-Process wuauclt -ArgumentList '/detectnow' -Verb RunAs"], check=True)
            update_progress(100)
            messagebox.showinfo("Siker", "A Windows Update keresése elindítva.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hiba", f"Hiba történt a Windows Update keresése közben: {e}")
        finally:
            update_progress(0)

    threading.Thread(target=update).start()

# Grafikus felület létrehozása
root = tk.Tk()
root.title("SySTool2025")

# Ablak mérete és felbontás
root.geometry("600x800")  # Állítsd be a kívánt méretet
root.resizable(False, False)  # Letiltja az ablak átméretezését

# Számítógépnév megjelenítése
computer_name = get_computer_name()
computer_name_label = tk.Label(root, text=f"Aktuális számítógépnév: {computer_name}")
computer_name_label.grid(row=0, column=0, columnspan=2, pady=10)

# Számítógépnév változtatása
hostname_label = tk.Label(root, text="Új számítógépnév:")
hostname_label.grid(row=1, column=0, pady=5)

hostname_entry = tk.Entry(root)
hostname_entry.grid(row=1, column=1, pady=5)

hostname_button = tk.Button(root, text="Számítógépnév változtatása", command=change_hostname)
hostname_button.grid(row=2, column=0, columnspan=2, pady=10)

# IPv6 be- és kikapcsolása
ipv6_button = tk.Button(root, text="IPv6 be/kikapcsolása", command=toggle_ipv6)
ipv6_button.grid(row=3, column=0, columnspan=2, pady=10)

# Idő szinkronizálása magyarországi szerverrel
time_sync_button = tk.Button(root, text="Idő szinkronizálása (Magyarország)", command=sync_time)
time_sync_button.grid(row=4, column=0, columnspan=2, pady=10)

# SNMP szolgáltatás telepítése és bekapcsolása
snmp_button = tk.Button(root, text="SNMP telepítése és bekapcsolása", command=install_snmp)
snmp_button.grid(row=5, column=0, columnspan=2, pady=10)

# BitLocker kikapcsolása
bitlocker_button = tk.Button(root, text="BitLocker kikapcsolása", command=disable_bitlocker)
bitlocker_button.grid(row=6, column=0, columnspan=2, pady=10)

# Felhasználó hozzáadása
user_label = tk.Label(root, text="Felhasználónév:")
user_label.grid(row=7, column=0, pady=5)

user_entry = tk.Entry(root)
user_entry.grid(row=7, column=1, pady=5)

password_label = tk.Label(root, text="Jelszó:")
password_label.grid(row=8, column=0, pady=5)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=8, column=1, pady=5)

add_user_button = tk.Button(root, text="Felhasználó hozzáadása", command=add_user)
add_user_button.grid(row=9, column=0, columnspan=2, pady=10)

# SMBv1 protokoll bekapcsolása
smbv1_button = tk.Button(root, text="SMBv1 protokoll bekapcsolása", command=enable_smbv1)
smbv1_button.grid(row=10, column=0, columnspan=2, pady=10)

# Tartományhoz csatlakozás
domain_button = tk.Button(root, text="Tartományhoz csatlakozás", command=join_domain)
domain_button.grid(row=11, column=0, columnspan=2, pady=10)

# Rendszerinformációk lekérése
system_info_button = tk.Button(root, text="Rendszerinformációk", command=get_system_info)
system_info_button.grid(row=12, column=0, columnspan=2, pady=10)

# Tűzfal bekapcsolása
firewall_enable_button = tk.Button(root, text="Tűzfal bekapcsolása", command=enable_firewall)
firewall_enable_button.grid(row=13, column=0, columnspan=2, pady=10)

# Tűzfal kikapcsolása
firewall_disable_button = tk.Button(root, text="Tűzfal kikapcsolása", command=disable_firewall)
firewall_disable_button.grid(row=14, column=0, columnspan=2, pady=10)

# Távoli asztal bekapcsolása
remote_desktop_button = tk.Button(root, text="Távoli asztal bekapcsolása", command=enable_remote_desktop)
remote_desktop_button.grid(row=15, column=0, columnspan=2, pady=10)

# Windows Update keresése
windows_update_button = tk.Button(root, text="Windows Update keresése", command=run_windows_update)
windows_update_button.grid(row=16, column=0, columnspan=2, pady=10)

# Folyamatcsík
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.grid(row=17, column=0, columnspan=2, pady=20)

# Lábléc hozzáadása
footer_label = tk.Label(root, text="SySTool2025 @ HiT", font=("Arial", 8), fg="gray")
footer_label.grid(row=18, column=0, columnspan=2, pady=10)

# Főciklus indítása
root.mainloop()
