# DuckDNS IP Updater

**Automatically update your DuckDNS domain with your public IPv4/IPv6 using a Python script.**

This project provides a Python script to monitor your public IP address and update your DuckDNS domain whenever it changes. It is designed to run as a cron job on Linux systems.

---

## Features

- Monitors both **IPv4** and **IPv6** public addresses.
- Updates DuckDNS automatically when your IP changes.
- Logs all activities to `log.txt`.
- Configurable via `config.txt`.
- Auto-configures a cron job for periodic execution.

---

## Requirements

- Python 3.6+
- `requests` library
- Linux system (for cron job setup)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/duckdns-updater.git
   cd duckdns-updater
   ```

---
2. **Install dependencies:**


   ```bash
   pip install -r requirements.txt
   ```

---
3. **Configure the script:**

Edit the config.txt file with your DuckDNS token and domain (or simply rename the config-example.txt and edit with your info):

    ```bash
    {"apikey": "your_duckdns_token", "domain": "your_domain", "ipv4": null, "ipv6": null }
   ```

---
**Usage**

1. **Run the script manually:**

    ```bash
    python3 main.py
   ```
---
2. **Set up the cron job (automatic execution):**

The script will attempt to set up a cron job to run every 5 minutes. If it fails due to permissions, you can manually add the following line to your crontab:

    ```bash
    */5 * * * * /usr/bin/python3 /path/to/programa.py >> /var/log/ip_updater.log 2>&1
   ```
---
**Configuration**

The config.txt file stores your DuckDNS token, domain, and the last known public IPs. The script updates this file whenever your IP changes.
Example config.txt:
```bash
    {
    "apikey": "12345678-90ab-cdef-1234-567890abcdef",
    "domain": "myhome",
    "ipv4": "123.45.67.89",
    "ipv6": null
}
   ```

**Logging**

All script activities are logged to log.txt. The log includes timestamps and detailed messages about IP changes and update attempts.
Example log entry:

```bash
2025-10-18 12:34:56,789 - INFO - --- Start of execution: 2025-10-18 12:34:56.789123 ---
2025-10-18 12:34:56,790 - INFO - Current IPv4: 123.45.67.89, Current IPv6: None
2025-10-18 12:34:56,790 - INFO - Last IPv4: 123.45.67.89, Last IPv6: None
2025-10-18 12:34:56,790 - INFO - IP unchanged. No update needed.    
   ```


**Troubleshooting**

- Permission issues: If the script fails to set up the cron job, run it as root or manually configure the cron job.
- DuckDNS API errors: Ensure your DuckDNS token is correct and your domain is properly configured.
- Log file not created: Check write permissions in the script's directory.


**License**

This project is licensed under the MIT License. See the LICENSE file for details.

**Contributing**

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


**Contact**

For questions or feedback, please contact me [giacconidev].








