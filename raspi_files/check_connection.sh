INTERFACE_NAME=$(iwconfig 2>/dev/null | grep -o "^\w*")

sleep 25;

if ifconfig $INTERFACE_NAME | grep -q "inet addr"
then
    echo "$(date) - connected" >> /home/pi/time.log
    # if connected check if it's ad hoc mode or not
    if iwconfig $INTERFACE_NAME | grep -q "Mode:Ad-Hoc"
    then
        echo "$(date) - start dhcp server" >> /home/pi/time.log
        # if running in ad hoc mode make sure server starts
        sudo service isc-dhcp-server start
    fi
else
    echo "$(date) - not connected" >> /home/pi/time.log
    # if not connected switch settings to ad hoc and reboot
    sudo cp /etc/network/interfaces-adhoc /etc/network/interfaces
    sudo reboot
fi

