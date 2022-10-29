from flask import Flask
from threading import Thread

app = Flask(' ')

@app.route("/")
def home():
    return "机器人已上线"

def run():
    app.run(host='0.0.0.0', port = 8800)

def keep_alive():
    t = Thread(target=run)
    t.start()