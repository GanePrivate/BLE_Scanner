import blescan
import sys
import time
import subprocess
import bluetooth._bluetooth as bluez
import datetime

cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell=True).decode('utf-8').rstrip('\n')

path_w = IP + '.csv'
datalist = []

def write_file(data):
    with open(path_w, mode='a') as f:
        for i in data:
            f.write(str(i))

dev_id = 1
try:
    sock = bluez.hci_open_dev(dev_id)
    print"ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

time_sta = time.time()

while True:
    elapsed_time = time.time() - time_sta
    if elapsed_time >= 180:
        write_file(datalist)
        print "finish"
        break
    returnedList = blescan.parse_events(sock, 10)
    for beacon in returnedList:
        if beacon.split(',')[1] == 'e7d61ea3f8dd49c88f2ff2484c07acb9' and beacon.split(',')[2] == '1' and beacon.split(',')[3] == '81':
            print "----------"
            rssi = beacon.split(',')[5]
            # print str(elapsed_time) + 's : ' + rssi + ',' + str(10**((-70 - float(rssi)) / 20))
            now = datetime.datetime.now()
            nowtime = now.strftime('%H:%M:%S.%f')
            datalist.append(str(nowtime) + ',' + rssi + ',' + str(10**((-70 - float(rssi)) / 20)) + '\n')
