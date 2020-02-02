from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask import request
import json
import threading
import subprocess
import time
import datetime
# from beacontools import BeaconScanner, IBeaconFilter

app = Flask(__name__)
CORS(app) # クロスドメインのエラー対策

path_w = './ble.csv'
BleGetFlag = True
start = 0
datalist = []


# スキャン結果をファイルに書き込む
def write_file(data):
    with open(path_w, mode='a') as f:
        # f.write('受信時間,経過時間(秒),MACアドレス,受信強度(rssi),送信強度,uuid,major,minor,uuid,major,minor\n')
        for i in data:
            f.write(str(i))


def callback(bt_addr, rssi, packet, additional_info):
    global BleGetFlag, start

    if BleGetFlag:
        start = time.time()
        BleGetFlag = False

    # 経過時間を計算
    elapsed_time = int(time.time() - start)
    # 現在の年月日時間情報取得
    now = datetime.datetime.now()

    nowtime = now.strftime('%H:%M:%S.%f')

    # data = nowtime + "," + str(elapsed_time) + "," + str(bt_addr) + "," + str(rssi) + "," + str(packet) + "," + str(additional_info) + "\n"
    data = nowtime + ","  + str(rssi)+ "\n"
    print("{} :: <{}, {}> {}".format(nowtime, bt_addr, rssi, packet))
    datalist.append(data)
    print("経過時間：{}秒".format(elapsed_time))
    print('{}m'.format(10**((-70 - rssi) / 20)))


@app.route("/command", methods=['GET'])
def main():
    if request.args.get('start') == 'true':
        print('OK!!!')
        # scan for all iBeacon advertisements from beacons with the specified uuid
        # scanner = BeaconScanner(
        #     callback,
        #     device_filter=IBeaconFilter(uuid="e7d61ea3-f8dd-49c8-8f2f-f2484c07acb9", major=7436, minor=17873)
        # )

        # scanner.start()
        # time.sleep(15)
        # scanner.stop()
        # write_file(datalist)
        return make_response(request.data)


app.run(host="127.0.0.1", port=6002)