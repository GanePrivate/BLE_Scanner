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
    print(request.args.get('start'))
    return make_response(request.data)


app.run(host="127.0.0.1", port=6001)
#threaded=True

# curl -X GET http://127.0.0.1:6001/command?start=true\&option=null
# git clone https://GanePrivate@github.com/BLE_Scanner.git
# git pull https://github.com/GanePrivate/BLE_Scanner