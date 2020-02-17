import subprocess
import time
import datetime
from beacontools import BeaconScanner, IBeaconFilter
import shutil


# 自分のIPアドレスを取得する
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell=True).decode('utf-8').rstrip('\n')

path_w = IP + '.csv'
BleGetFlag = True
start = 0
datalist = []


# スキャン結果をファイルに書き込む
def write_file(data):
    # csvファイルに結果を書き出す
    with open(path_w, mode='a') as f:
        # f.write('受信時間,経過時間(秒),MACアドレス,受信強度(rssi),送信強度,uuid,major,minor,uuid,major,minor\n')
        for i in data:
            f.write(str(i))
    shutil.move(path_w, '/run/user/1000/gvfs/smb-share:server=192.168.10.2,share=ble_data')


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
    data = nowtime + ","  + str(rssi) + "," + str(10**((-70 - rssi) / 20)) + "\n"
    # print("{} :: <{}, {}> {}".format(nowtime, bt_addr, rssi, packet))
    print("{} : {}dBm, {}m".format(nowtime, rssi, 10**((-70 - rssi) / 20)))
    datalist.append(data)
    # print("経過時間：{}秒".format(elapsed_time))
    # print('{}m'.format(10**((-70 - rssi) / 20)))


def main():
    # scan for all iBeacon advertisements from beacons with the specified uuid
    scanner = BeaconScanner(
        callback,
        device_filter=IBeaconFilter(uuid="e7d61ea3-f8dd-49c8-8f2f-f2484c07acb9", major=7436, minor=17873)
    )

    scanner.start()
    time.sleep(15)
    scanner.stop()
    write_file(datalist)


if __name__ == '__main__':
    main()