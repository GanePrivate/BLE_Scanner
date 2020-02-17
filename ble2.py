import blescan
import sys
import time

import bluetooth._bluetooth as bluez

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print"ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

# 時間計測開始
time_sta = time.perf_counter()

while True:
    if time.perf_counter() - time_sta >= 10:
        print "finish"
        break
    returnedList = blescan.parse_events(sock, 10)
    for beacon in returnedList:
        if beacon.split(',')[1] == 'e7d61ea3f8dd49c88f2ff2484c07acb9' and beacon.split(',')[2] == '1' and beacon.split(',')[3] == '81':
            print "----------"
            print beacon