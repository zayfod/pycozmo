Capturing Cozmo Communication
=============================


Overview
--------

Capturing the communication between the Cozmo app and Cozmo is very valuable for understanding how Cozmo works.

One way to achieve this is by placing a Linux machine between the two as shown on the following diagram.

```

+---------------+         Wi-Fi          +---------------+          Wi-Fi         +---------------+
|               |                        |               |                        |               |
| Mobile Device | ---------------------> | Linux Machine | ---------------------> |     Cozmo     |
|               |                  wlan1 |               | wlan0                  |               |
+---------------+                        +---------------+                        +---------------+

```

The Linux machine acts as a Wi-Fi client on one interface (wlan0) and associates with Cozmo. It acts as a Wi-Fi access
point (AP) on the other interface and allows a mobile device, running the Cozmo app to associate with it.

With appropriate network configuration such a setup allows capturing Cozmo communication in
[pcap files](https://en.wikipedia.org/wiki/Pcap) using tcpdump.


Prerequisites
-------------

- [Cozmo robot](https://www.digitaldreamlabs.com/pages/cozmo)
- Mobile device with the [Cozmo app](https://play.google.com/store/apps/details?id=com.anki.cozmo)
- (Ubuntu) Linux machine with 2 Wi-Fi interfaces (e.g. a Raspberry Pi)
- The following tools installed:
    - [wireless-tools](https://en.wikipedia.org/wiki/Wireless_tools_for_Linux)
    - [wpa_supplicant](https://en.wikipedia.org/wiki/Wpa_supplicant)
    - [hostapd](https://en.wikipedia.org/wiki/Hostapd)
    - [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq)
    - [tcpdump](https://en.wikipedia.org/wiki/Tcpdump)


Connecting to Cozmo
-------------------

Ensure that wireless tools and wpa_supplicant are installed.
```
$ sudo apt-get install wireless-tools wpasupplicant
```

Wake up Cozmo but placing it on the charging platform.

Make Cozmo display it's Wi-Fi PSK key by rising and lowering its lift.

Get Cozmo's Wi-Fi SSID by scanning for Wi-Fi devices:
```
$ sudo iwlist wlan0 scan
wlan0     Scan completed :
          Cell 01 - Address: 5E:CF:7F:XX:XX:XX
                    ESSID:"Cozmo_XXXXXX"
                    Protocol:IEEE 802.11bg
                    Mode:Master
                    Frequency:2.412 GHz (Channel 1)
                    Encryption key:on
                    Bit Rates:54 Mb/s
                    Extra:rsn_ie=30180100000fac020200000fac04000fac020100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : PSK
                    Quality=100/100  Signal level=100/100  
```

Open wpa_supplicant's [configuration file](https://linux.die.net/man/5/wpa_supplicant.conf):
```
$ sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
```

Configure wpa_supplicant to automatically connect to Cozmo by adding the following:
``` 
network={
    ssid="Cozmo_XXXXXX"
    psk="XXXXXXXXXXXX"
}
```

Load the new configuration (or reboot):
```
$ sudo wpa_cli -i wlan0 reconfigure
OK
```

At this point the Linux machine should be associated with Cozmo: 
```
$ ip addr
...
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 80:1f:02:XX:XX:XX brd ff:ff:ff:ff:ff:ff
    inet 172.31.1.172/24 brd 172.31.1.255 scope global wlan0
       valid_lft forever preferred_lft forever
    inet6 fe80::1d4b:9d3b:c6f0:f5b1/64 scope link 
       valid_lft forever preferred_lft forever
```

Cozmo should respond to ping:
```
$ ping 172.31.1.1
PING 172.31.1.1 (172.31.1.1) 56(84) bytes of data.
64 bytes from 172.31.1.1: icmp_seq=1 ttl=128 time=1.94 ms
64 bytes from 172.31.1.1: icmp_seq=2 ttl=128 time=2.28 ms
...
```


Masquerading as a Cozmo
-----------------------

Install hostapd and dnsmasq:
```
$ sudo apt-get install hostapd dnsmasq
```

Edit dhcpdcd`s [configuration file](https://manpages.ubuntu.com/manpages/trusty/man5/dhcpcd.conf.5.html):
```
$ sudo vi /etc/dhcpcd.conf
```

Disable wpa_supplicant on wlan1 and configure a static IP address by adding the following:
```
interface wlan1
nohook wpa_supplicant
static ip_address=192.168.50.1/24
```

Edit dnsmasq's [configuration file](https://linux.die.net/man/8/dnsmasq):
```
$ sudo vi /etc/dnsmasq.conf
```

Configure DHCP on wlan1 by adding the following:
```
interface=wlan1
dhcp-range=192.168.50.50,192.168.50.100,255.255.255.0,24h
```

Restart dnsmasq
```
$ sudo systemctl start dnsmasq
```

Create a configuration file for hostapd:
```
$ sudo vi /etc/hostapd/hostapd.conf 
```

Configure a Wi-Fi AP with WPA2 PSK on wlan1 by adding the following:
```
interface=wlan1
hw_mode=g
channel=1
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=Cozmo_111111
wpa_passphrase=XXXXXXXXXXXX
```

The SSID should be different from Cozmo's SSID and should follow the form `Cozmo_XXXXXX`, where XXXXXX are
upper-case hexadecimal digits as this is what the Cozmo app looks for.

The passphrase should consist of exactly 12 upper-case hexadecimal digits as this is what the Cozmo app expects.

Edit `/etc/default/hostapd`:
```
$ sudo vi /etc/default/hostapd
```

Configure the newly created configuration file:
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

Enable and start hostapd:
```
$ sudo systemctl unmask hostapd
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
```

Ensure that IP forwarding is enabled on boot:
```
$ sudo vi /etc/sysctl.conf
```

The following line should be uncommented:
```
net.ipv4.ip_forward=1
```

Ensure that IP forwarding is enabled:
```
$ sudo sysctl net.ipv4.ip_forward=1
```

The Cozmo app always tries to communicate with Cozmo using the IP address 172.31.1.1 .

Configure masquerading on wlan0 so that packets, coming from the Cozmo app, with source IP in the range 192.168.50.0/24,
reach Cozmo with the wlan0 IP address of the Linux machine.
```
$ sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
```

This is necessary, because Cozmo only responds to UDP packets with source IP address in the range 172.31.1.0/24 . 


Capturing Communication
-----------------------

Ensure that tcpdump is installed:
```
$ sudo apt-get install tcpdump
```

At this point, it should be possible to capture Cozmo communication using tcpdump:
```
$ sudo tcpdump -i wlan0 -w cozmo.pcap
```

Connect to cozmo from the app. The app should find at least 2 Cozmos (one being the masqueraded Linux machine) and a
selection screen should show up.

The captured PCAP file can be analyzed with [Wireshark](https://en.wikipedia.org/wiki/Wireshark) or with
`pycozmo_dump.py`.
