import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Magyar ISP-k IPv4 tartományai (példa)
isp_ip_ranges = [
    "81.183.0.0/16",  # UPC
    "94.21.0.0/16",   # Telekom
    "91.82.0.0/16",   # Digi
    "31.46.0.0/16",   # Invitel
]

# Traceroute futtatása egy IP címre
def run_traceroute(ip):
    try:
        # Linux/Mac esetén 'traceroute', Windows esetén 'tracert'
        command = ["traceroute", "-m", "30", ip]  # '-m 30': maximális hopok száma
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Hiba a traceroute futtatásakor: {e}"

# Csomagvesztés kiszámítása a traceroute kimenetből
def calculate_packet_loss(traceroute_output):
    lines = traceroute_output.splitlines()
    total_hops = len(lines) - 1  # Az első sor nem hop
    lost_packets = 0

    for line in lines[1:]:  # Az első sor kihagyása
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
def main():
    results = []

    # Traceroute futtatása párhuzamosan
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip_range in isp_ip_ranges:
            ips = generate_ips_from_range(ip_range)
            futures = [executor.submit(run_traceroute, ip) for ip in ips]

            for future in futures:
                traceroute_output = future.result()
                packet_loss = calculate_packet_loss(traceroute_output)
                results.append({"IP": ip, "Packet Loss (%)": packet_loss})

    # Eredmények tárolása DataFrame-be
    df = pd.DataFrame(results)
    print(df)

    # Statisztikák ábrázolása
    df.plot(kind="bar", x="IP", y="Packet Loss (%)", legend=False)
    plt.title("Csomagvesztés statisztika")
    plt.xlabel("IP cím")
    plt.ylabel("Csomagvesztés (%)")
    plt.show()

if __name__ == "__main__":
    main()
