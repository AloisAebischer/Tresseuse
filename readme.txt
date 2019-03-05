1 ###Connect to RD wifi###
-sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
-Edit file as such:

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev update_config=1
country=CH

network={
        ssid="RD"
        psk="wifi4RND"
        key_mgmt=WPA2-PSK
}

-sudo reboot
######

2 ###Install Yoctopuce library###
-If not the case, download the YoctoLib.python.2987 and place it in the Projet-Tresseuse folder
######

3 ###Install PyQt4 package###
-sudo apt-get install python-qt4
######

4 ###Create wifi access point###
-Follow this tutorial:
https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/
-Set yocto-wifi:
	SSID:Pi3
	PSK:raspberry
	ip: 172.24.1.2/3
-Carefull with yocto serial names!
######

5 ###Make the app runnable###
-Navigate in the terminal to the Projet-Tresseuse folder
-sudo chmod +x run.sh
######

6 ###Install LCD-Touchscreen drivers###
-sudo nano /boot/config.txt
-Append the following lines at the bottom:

#Uncomment to set LCD screen set up
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 800 480 60 6 0 0 0

-Navigate in the terminal to the Projet-Tresseuse folder
-Install the drivers with the following commands:

tar xzvf joy-IT-lcd5-driver.tar.gz (if the LCD-show folder has not been decompressed yet)
cd LCD-show/
sudo bash ./LCD5-show

-reboot with the LCD-Touchscreen plugged
######

7 ###Appair bluetooth mouse###

Double click on run.sh






