#!/bin/bash
echo "[*] Setting up Apex Framework..."
sudo apt update
sudo apt install -y nmap tor proxychains4 metasploit-framework python3-pip curl
pip3 install python-nmap shodan pymetasploit3 colorama requests flask --break-system-packages

# Setup ProxyChains
sudo sed -i 's/socks4 \t127.0.0.1 9050/socks5 \t127.0.0.1 9050/' /etc/proxychains4.conf
sudo service tor start

echo "[+] Done. Remember to start msfrpcd before running core.py"
