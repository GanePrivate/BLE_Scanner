from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask import request
import json
import threading
import subprocess


app = Flask(__name__)
CORS(app) # クロスドメインのエラー対策


@app.route("/command", methods=['GET'])
def webhook():
    # URLパラメータ
    params = request.args
    # print(params)
    # print(request.data)
    # print(request.args.get('start'))

    # startコマンドが来たらBLEビーコンのスキャン・受信を実行
    if request.args.get('start') == 'true':
        cmd = "sudo python3 ble.py"
        subprocess.call(cmd.split())

    # pullコマンドが来たら変更点をpullする
    if request.args.get('pull') == 'true':
        cmd = "git pull"
        subprocess.call(cmd.split())
    return make_response(request.data)


app.run(host="192.168.1.5", port=7000)
#threaded=True

# curl -X GET http://127.0.0.1:7000/command?start=true\&pull=true
# git clone https://github.com/GanePrivate/BLE_Scanner.git
# git pull