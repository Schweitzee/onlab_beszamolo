#!/bin/bash
echo "Elindult a h3 szkript!"
sleep 2
./libquicr/build/cmd/examples/qclient -r moq://172.16.0.100:1234 --pub_namespace clock --pub_name second --clock
bash  # <-- ez nyitva tartja a terminált a végén
