# Wi-Fi Brute-Force Scanner

> **⚠️ IMPORTANT DISCLAIMER**

> This project is a **little experiment** created purely for **educational and technical purposes**. It was written as a way for me to learn how important **hardened security** is — precisely because tools like this exist. I do **not** recommend anybody to try it on networks you do not own or have explicit permission to test. Unauthorized access to a network is illegal in most jurisdictions and can carry serious legal consequences.

## About

`wifi-connect.py` is a small Python script that:

1. Scans for nearby Wi-Fi networks.
2. Loads a list of candidate passwords from a text file.
3. Attempts to connect to discovered networks using those passwords (brute-force).

The whole point of this project is to demonstrate *why* strong, unique Wi-Fi passwords and properly hardened network security matter. Weak and predictable passwords are the bare minimum defense against such scripts.

## Features

- **Scan** nearby Wi-Fi networks and deduplicate multi-band SSIDs.
- **Load** passwords from a plain text file.
- **Brute-force** all discovered networks or a single chosen target.
- Clean up profiles after failed attempts.

## Requirements

- Python 3.8+
- Windows (recommended) — 
- `pywifi` (and its underlying dependencies, e.g. `python3-wifi`)
- A compatible wireless adapter

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Install the requirements (see above).
2. Create a `passwords.txt` file in the same directory, with one candidate password per line.
3. Run the script with root privileges:

```bash
 python3 connect-wifi.py
```

4. Follow the prompts to choose between brute-forcing **all** discovered networks or a **single** one.

## Project Structure

```
wifi_bruteforce/
├── connect-wifi.py          # Main script
├── passwords.txt       # Your candidate password list (one per line)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Legal & Ethical Notice

This tool is intended **only** for:

- Testing your **own** networks and devices.
- Authorized penetration testing / security auditing engagements.
- Educational study of Wi-Fi security concepts.

**Using this tool against any network without explicit permission is illegal.** I do not recommend or condone it, and I am not responsible for any misuse. If you use this tool, you are solely responsible for complying with all applicable laws and rules where you live.
