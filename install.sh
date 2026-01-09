#!/bin/bash
sudo apt update && sudo apt install -y nmap tor proxychains4 metasploit-framework python3-pip stem curl
pip3 install python-nmap shodan pymetasploit3 colorama requests flask python-telegram-bot --break-system-packages
sudo sed -i 's/socks4 \t127.0.0.1 9050/socks5 \t127.0.0.1 9050/' /etc/proxychains4.conf
sudo service tor start
