import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Magyar ISP-k IPv4 tartományai (példa)
isp_ip_ranges = [
    "81.183.0.0/16",  # UPC
    "94.21.0.0/16",   # Telekom
    "91.82.0.0/16",   # Digi
    "31.46.0.0/16",   # Invitel
]

# Tracert futtatása egy IP címre (Windows alatt)
def run_tracert(ip):
    try:
        command = ["tracert", "-h", "30", ip]  # '-h 30': maximális hopok száma
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        return result.stdout
    except Exception as e:
        return f"Hiba a tracert futtatásakor: {e}"

# Csomagvesztés kiszámítása a tracert kimenetből
def calculate_packet_loss(tracert_output):
    lines = tracert_output.splitlines()
    total_hops = len(lines) - 4  # Az első 4 sor nem hop (fejléc és üres sorok)
    lost_packets = 0

    for line in lines[4:]:  # Az első 4 sor kihagyása
        if "* * *" in line:  # Csomagvesztés jelzése
            lost_packets += 1

    if total_hops == 0:
        return 0
    return (lost_packets / total_hops) * 100  # Csomagvesztés százalékban

# IP címek generálása egy tartományból (egyszerűsített példa)
def generate_ips_from_range(ip_range):
    # Példa: csak az első 10 IP cím
    base_ip = ip_range.split('/')[0]
    return [f"{base_ip[:-1]}{i}" for i in range(1, 11)]

# Fő folyamat
def start_analysis():
    results = []

    # Tracert futtatása párhuzamosan
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip_range in isp_ip_ranges:
            ips = generate_ips_from_range(ip_range)
            futures = [executor.submit(run_tracert, ip) for ip in ips]

            for future in futures:
                tracert_output = future.result()
                packet_loss = calculate_packet_loss(tracert_output)
                results.append({"IP": ip, "Packet Loss (%)": packet_loss})

    # Eredmények tárolása DataFrame-be
    df = pd.DataFrame(results)
    display_results(df)

# Eredmények megjelenítése
def display_results(df):
    # Táblázat megjelenítése
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", "end", values=(row["IP"], row["Packet Loss (%)"]))

    # Grafikon megjelenítése
    fig, ax = plt.subplots()
    df.plot(kind="bar", x="IP", y="Packet Loss (%)", legend=False, ax=ax)
    ax.set_title("Csomagvesztés statisztika")
    ax.set_xlabel("IP cím")
    ax.set_ylabel("Csomagvesztés (%)")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI inicializálása
root = tk.Tk()
root.title("Traceroute Analizátor")

# Fő keret
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Táblázat keret
table_frame = ttk.Frame(main_frame)
table_frame.pack(fill=tk.X, pady=10)

# Táblázat létrehozása
columns = ("IP", "Packet Loss (%)")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.heading("IP", text="IP cím")
tree.heading("Packet Loss (%)", text="Csomagvesztés (%)")
tree.pack(fill=tk.X)

# Grafikon keret
graph_frame = ttk.Frame(main_frame)
graph_frame.pack(fill=tk.BOTH, expand=True)

# Start gomb
start_button = ttk.Button(main_frame, text="Elemzés indítása", command=start_analysis)
start_button.pack(pady=10)

# Fő ciklus indítása
root.mainloop()
