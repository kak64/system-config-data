# 🚀 Apex Predator v11.0 - Stealth Red Team Framework

**Apex Predator** is a modular, high-performance automation suite built for stealthy reconnaissance and exploitation. It integrates Nmap, Metasploit, and Telegram API into a single command-and-control (C2) workflow.



---

## 🛡️ Key Capabilities
* **Full-Spectrum Recon:** Port scanning and service fingerprinting over the Tor network.
* **Auto-Exploitation:** Direct integration with Metasploit RPC for zero-click module execution.
* **Credential Harvesting:** Flask-based phishing engine with real-time Telegram exfiltration.
* **Maximum Anonymity:** Pre-configured for ProxyChains and SOCKS5 routing.
* **Instant Notifications:** Get success alerts and captured credentials sent straight to your phone.

---

## 📂 Project Structure
* `core.py` - The main exploitation engine and scanner.
* `phish.py` - The phishing server and credential harvester.
* `install.sh` - Automated environment setup for Linux/VPS.
* `requirements.txt` - Python dependency list.

---

## 🚀 Rapid Deployment

1. **Clone the Private Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/system-config-data.git](https://github.com/YOUR_USERNAME/system-config-data.git)
   cd system-config-data

2. Run Automatic Setup:
3. chmod +x install.sh
./install.sh

3. Set Up the C2 Brain (Metasploit RPC):
4. msfrpcd -P mypassword -S -a 127.0.0.1

⚙️ Operational Configuration
Before launching, ensure you have updated the CONFIG section in core.py and phish.py:

Shodan Key: For passive infrastructure data.

Telegram Token: Your bot's API token from @BotFather.

Chat ID: Your unique user ID for private alerts.

🎮 Execution Commands
Mode 1: Recon & Exploit
To attack a target (IP or Domain) while staying anonymous:
proxychains4 python3 core.py

Mode 2: Phishing Mode
To host a phishing page and capture login data:
python3 phish.py

Note: Use Ngrok to expose port 8080 to the internet.

🛡️ OPSEC Guidelines
Always verify Tor status before execution: proxychains4 curl ifconfig.me.

Use Private Repositories only to protect your API keys.

Regularly clear command history: history -c.

⚠️ Legal Disclaimer
This framework is developed for educational purposes and authorized penetration testing only. Unauthorized use against systems is illegal and strictly prohibited. The developer is not responsible for any misuse.




