Cozmo Protocol
==============


Overview
--------

The Cozmo protocol is a UDP-based variant of the
[selective repeat automatic-repeat request (ARQ) protocol](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ).

The Cozmo app (aka "engine") acts as a client and Cozmo (aka "robot") acts as a server.

The two exchange frames, encapsulated in UDP packets.

Each frame can contain 0, 1, or more packets.


Network Setup
-------------

The robot acts as a Wi-Fi access point. It always uses an SSID that follows the form "Cozmo_XXXXXX", where XXXXXX are
upper-case hexadecimal digits. It acts as a DHCP server and assigns Wi-Fi clients an IP address in the range
172.31.1.0/24 .

The app searches for robot APs. If it finds only one, it will associate with it automatically. If it finds more than
one, it will allow the user to select one manually.

The robot acts as a server. It always uses the IP address 172.31.1.1 and will expect UDP packets on port 5551.
It will only accept packets originating from an IP address in the range 172.31.1.0/24 .

The app acts as a client and initiates connections. It will only accept packets originating from the IP address
172.31.1.1 .

```
+--------------------+                        +--------------------+
|     Cozmo app      |                        |       Cozmo        |
|      "engine"      |        UDP/Wi-Fi       |      "robot"       |
|    Wi-Fi client    | +--------------------> |      Wi-Fi AP      |
|     UDP client     |                        |     UDP Server     |
+--------------------+                        +--------------------+
    172.31.1.0/24                                 172.31.1.1:5551
```


Frames
------

Each frame has the following structure:

```
Field           Length      Description
---------------------------------------------------------------------------------
id              7           Always "COZ\x03RE\x01"
type            1           Frame type
first_seq       2           First packet sequence number in the frame or 0
seq             2           Last packet sequence number in the frame or 0
ack             2           Peer packet sequence number acknowledgementz
packets         -           0 or more encapsulated packets
```

Frame types:

```
Type            Source      Description
---------------------------------------------------------------------------------
0x01            engine      Reset
0x02            robot       Reset ACK
0x03            engine      Disconnect
0x04            engine      Engine action
0x07            engine      Engine packets
0x09            robot       Robot packets
0x0b            engine      Out-of-band engine ping
```


Packets
-------

Packet types:

```
Type    OOB     Source      Description
---------------------------------------------------------------------------------
0x02    n       robot       Connect
0x03    n       engine      Disconnect
0x04    n       both        Action
0x05    y       robot       Event
0x0a    y       engine      Unknown
0x0b    y       engine      Ping
```

Out of band packets do not get assigned sequence IDs.

Packet content is Cozmo firmware version specific.


Connection Establishment
------------------------

The engine sends a reset frame (0x01) to the robot with first_seq and seq set to 1 and ack set to 0.

The robot responds with a robot packets frame (0x09) with first_seq and seq set to 1 and ack set to 1, containing a
connect packet (0x02). This establishes the connections.

The engine maintains the connection by periodically sending ping frames (0x0b). The robot responds with robot packet
frames (0x09), containing a copy of the engine's ping in a ping packet (0x0b). The pings have a sequence ID and a time
stamp and allow the engine to measure round-trip time.

If the robot stops receiving ping frames for more than 5 s it will disconnect and display the message "COZMO 01".

The engine can gracefully close the connection in one of two ways:
- by sending a disconnect frame (0x03)
- by sending an engine packets frame (0x07), containing a disconnect packet (0x03).

As long as a connection is established, the engine and the robot can exchange packets.

The engine sends packets in frames of types 0x04 and 0x07.

The robot sends packets in frames of type 0x09.
