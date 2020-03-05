import subprocess
import time
import datetime
from beacontools import BeaconScanner, IBeaconFilter


# 自分のIPアドレスを取得する
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell=True).decode('utf-8').rstrip('\n')

path_w = IP + '.csv'
BleGetFlag = True
start = 0
datalist = []

tmp = datetime.datetime.now()
dt = datetime.datetime(tmp.year, tmp.month, tmp.day, tmp.hour, tmp.minute + 1)


# スキャン結果をファイルに書き込む
def write_file(data):
    # csvファイルに結果を書き出す
    with open(path_w, mode='a') as f:
        # f.write('受信時間,経過時間(秒),MACアドレス,受信強度(rssi),送信強度,uuid,major,minor,uuid,major,minor\n')
        for i in data:
            f.write(str(i))


def callback(bt_addr, rssi, packet, additional_info):
    global BleGetFlag, start, dt

    while:
        if datetime.datetime.now() >= dt:
            break

    if BleGetFlag:
        start = time.time()
        BleGetFlag = False

    # 経過時間を計算
    elapsed_time = int(time.time() - start)
    # 現在の年月日時間情報取得
    start_time = datetime.datetime.now()+datetime.timedelta(milliseconds=100)
    if datetime.datetime.now() ==  start_time:
        nowtime = start_time.strftime('%H:%M:%S.%f')
        # data = nowtime + "," + str(elapsed_time) + "," + str(bt_addr) + "," + str(rssi) + "," + str(packet) + "," + str(additional_info) + "\n"
        data = nowtime + ","  + str(rssi) + "," + str(10**((-70 - rssi) / 20)) + "\n"
        # print("{} :: <{}, {}> {}".format(nowtime, bt_addr, rssi, packet))
        # print("{} : {}dBm, {}m".format(nowtime, rssi, 10**((-70 - rssi) / 20)))
        datalist.append(data)
        # print("経過時間：{}秒".format(elapsed_time))
        # print('{}m'.format(10**((-70 - rssi) / 20)))


def main():
    # scan for all iBeacon advertisements from beacons with the specified uuid
    scanner = BeaconScanner(
        callback,
        device_filter=IBeaconFilter(uuid="e7d61ea3-f8dd-49c8-8f2f-f2484c07acb9", major=1, minor=81)
    )

    scanner.start()
    time.sleep(120)
    scanner.stop()
    write_file(datalist)
    print('fin')


if __name__ == '__main__':
    main()