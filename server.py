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
    if request.args.get('start') == 'true':
        cmd = "git pull"
        subprocess.call(cmd.split())
    if request.args.get('option') == 'true':
        cmd = "curl -X GET http://127.0.0.1:6002/command?start=true"
        subprocess.call(cmd.split())
    return make_response(request.data)


app.run(host="127.0.0.1", port=6001)
#threaded=True

# curl -X GET http://127.0.0.1:6001/command?start=true\&option=null
# git clone https://github.com/GanePrivate/BLE_Scanner.git
# git pull