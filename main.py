import logging
import requests
import schedule
import time
import os
import json
import socket
from pathlib import Path

# config file
CONFIG_FILE = "config.txt"
# log file
LOG_FILE = "log.txt"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()  # También imprime en consola
        ]
    )

def get_public_ipv4():
    try:
        return requests.get('https://api.ipify.org?format=json', timeout=5).json()['ip']
    except:
        return None

def get_public_ipv6():
    try:
        return requests.get('https://api6.ipify.org?format=json', timeout=5).json()['ip']
    except:
        return None

def load_config_from_file():
    if not Path(CONFIG_FILE).exists():
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not exists.")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_last_ips(apikey, domain, ipv4, ipv6):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"apikey": apikey, "domain": domain, "ipv4": ipv4, "ipv6": ipv6}, f)

def update_dns(ipv4, ipv6, api_key, domain): # only ipv4 at the moment
    url = f"https://www.duckdns.org/update?domains={domain}&token={api_key}&ip={ipv4}"
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False
    
def get_ip_from_domain(domain):
    try:
        # Resuelve el dominio a IPv4
        ipv4 = socket.gethostbyname(domain)
        # Resuelve el dominio a IPv6 (si está disponible)
        try:
            ipv6 = socket.getaddrinfo(domain, None, socket.AF_INET6)[0][4][0]
        except:
            ipv6 = None
        return ipv4, ipv6
    except socket.gaierror:
        return None, None

def main():
    setup_logging()
    # Load config from file
    config = load_config_from_file()

    # Get current IPs
    current_ipv4 = get_public_ipv4()
    current_ipv6 = get_public_ipv6()

    logging.info(f"IPv4 actual: {current_ipv4}, IPv6 actual: {current_ipv6}")
    logging.info(f"Última IPv4: {config['ipv4']}, Última IPv6: {config['ipv6']}")

    # Compare and update if changed
    if (current_ipv4 != config['ipv4']) or (current_ipv6 != config['ipv6']):
        logging.info("IP changed. Updating DNS...")
        success = update_dns(current_ipv4, current_ipv6, config['apikey'], config['domain'])
        if success:
            save_last_ips(config['apikey'], config['domain'], current_ipv4, current_ipv6)
            logging.info("DNS updated correctly.")
        else:
            logging.info("Error updating DNS.")

        logging.info("checking domain resolution...")
        resolved_ipv4, resolved_ipv6 = get_ip_from_domain(config['domain'] + ".duckdns.org")
        logging.info(f"Domain resolved IPv4: {resolved_ipv4}, IPv6: {resolved_ipv6}")
    else:
        logging.info("No IP changes, we not update DNS.")

# Ejecutar cada 5 minutos
schedule.every(5).minutes.do(main)

# Configurar el cron job automáticamente (solo para Linux)
def setup_cron_job():
    script_path = os.path.abspath(__file__)
    cron_job = f"*/5 * * * * /usr/bin/python3 {script_path} >> /var/log/ip_updater.log 2>&1\n"
    try:
        with open("/etc/crontab", "r") as f:
            crontab = f.read()
        if "ip_updater.log" not in crontab:
            with open("/etc/crontab", "a") as f:
                f.write(cron_job)
            logging.info("Cron job configured correctly.")
        else:
            logging.info("Cron job  already exists.")
    except PermissionError:
        logging.info("Error: No permission granted to change /etc/crontab. Execute with root privilegies or manually insert into crontab.")

if __name__ == "__main__":
    # Configurar el cron job al ejecutar el script por primera vez
    # setup_cron_job()
    # Ejecutar el main una vez al inicio
    main()
    # Mantener el script corriendo para el schedule
    while True:
        schedule.run_pending()
        time.sleep(1)
