#!/bin/bash
# curl http://192.168.10.5:7000/hello
# curl http://192.168.10.6:7000/hello
# curl http://192.168.10.7:7000/hello
# curl http://192.168.10.8:7000/hello

curl http://192.168.10.5:7000/start &
curl http://192.168.10.6:7000/start &
curl http://192.168.10.7:7000/start &
curl http://192.168.10.8:7000/start &