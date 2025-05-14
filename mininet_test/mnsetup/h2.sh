#!/bin/bash
echo "Elindult a h2 szkript!"
sleep 2
./libquicr/build/cmd/examples/qserver -k server-key.pem -c server-cert.pem --bind_ip 172.16.0.100 -m
bash  # <-- ez nyitva tartja a terminált a végén
