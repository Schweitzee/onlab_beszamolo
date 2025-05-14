#!/bin/bash
echo "Elindult a h1 szkript!"
sleep 3
./libquicr/build/cmd/examples/qclient -r moq://172.16.0.100:1234 --sub_namespace clock --sub_name second -m -a 192.168.1.100/3,192.168.2.100/4                                  
bash  # <-- ez nyitva tartja a terminált a végén
