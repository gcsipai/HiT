from scapy.all import ARP, Ether, srp
import platform
import os

def ip_scan(network_range):
    # Create an ARP request packet
    arp = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and receive the response
    result = srp(packet, timeout=2, verbose=0)[0]

    # Parse the response
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def clear_screen():
    # Clear the terminal screen based on the OS
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    clear_screen()
    print("Gcsipai IP Scanner for Windows 11")
    print("-------------------------")

    # Define the network range to scan (e.g., "10.0.0.1/24")
    network_range = input("Enter the network range to scan (e.g., 10.0.0.1/24): ")

    print(f"\nScanning network {network_range}...\n")

    # Perform the IP scan
    devices = ip_scan(network_range)

    # Display the results
    if devices:
        print("Active devices on the network:")
        print("IP Address\t\tMAC Address")
        print("-----------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")

if __name__ == "__main__":
    main()
