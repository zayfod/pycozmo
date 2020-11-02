Cozmo Protocol
==============


Overview
--------

The Cozmo protocol is a UDP-based variant of the
[selective repeat automatic-repeat request (ARQ) protocol](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ).

The Cozmo app (aka "engine") acts as a client and Cozmo (aka "robot") acts as a server.

The two exchange frames, encapsulated in UDP packets.

Each frame can contain 0, 1, or more packets.

See `protocol_declaration.py` for packet details.


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
|    Wi-Fi client    | ---------------------> |      Wi-Fi AP      |
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
ack             2           Peer packet sequence number acknowledgement
packets         -           0 or more encapsulated packets
```

Frame types:

```
Type            Source      Description
---------------------------------------------------------------------------------
0x01            engine      Reset
0x02            robot       Reset ACK
0x03            engine      Disconnect
0x04            engine      Engine packet - single
0x07            engine      Engine packets - zero or more
0x09            robot       Robot packets - zero or more
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
0x04    n       both        Command
0x05    y       robot       Event
0x0a    y       engine      Keyframe
0x0b    y       engine      Ping
```

Out of band packets do not get assigned sequence IDs.

Packet content is Cozmo firmware version specific.

Commands and events are identified by an 8-bit ID. IDs in the range 0-0xaf are sent by the engine. IDs in the range
0xb0-0xff are sent by the robot.

IDs in the range 0xf0-0xff are used for out-of-band updates. These are packets that are not tracked by a sequence ID
and thus not retransmitted. Only their latest received value is considered important. 

```
ID                 Min     Max      Name
---------------------------------------------------------------------------------
0x03	     	    31	    31		LightStateCenter              
0x04	     	    40	    40		CubeLights                    
0x05	     	     5	     5		ObjectConnect                 
0x0b	     	     1	     1		SetHeadLight                  
0x0c	     	     1	     1		                              
0x10	     	     5	     5		CubeId                        
0x11	     	    21	    21		LightStateSide                
0x25	     	     0	     0		Enable                        
0x32	     	    16	    16		DriveWheels                   
0x33	     	    10	    10		TurnInPlaceAtSpeed                   
0x34	     	     4	     4		DriveLift                     
0x35	     	     4	     4		DriveHead                     
0x36	     	    17	    17		SetLiftHeight                 
0x37	     	    17	    17		SetHeadAngle                  
0x39	     	    20	    20		TurnInPlace                 
0x3b	     	     0	     0		StopAllMotors
0x3d								DriveStraight             
0x45	     	    24	    24		                              
0x4b	     	     8	     8		EnableBodyACC		                              
0x4c	     	     2	     2		EnableCamera                  
0x50	     	     2	     2		                              
0x54	     	     2	     2		                              
0x57	     	     7	     7		SetCameraParams               
0x60	     	     1	     1		EnableStopOnCliff             
0x64	     	     2	     2		SetRobotVolume                
0x66	     	     1	     1		EnableColorImages             
0x80	     	     4	     4		                              
0x81	     	    12	   144	*	NvStorageOp                   
0x8d	     	     0	     0		                              
0x8e	     	   744	   744		OutputAudio                   
0x8f	     	     0	     0		OutputSilence                     
0x93	     	     3	     3		                              
0x94	     	     3	     3		                              
0x97	     	     4	   188	*	DisplayImage                  
0x98	     	    10	    10		                              
0x99	     	     4	     4		                              
0x9a	     	     0	     0		                              
0x9b	     	     1	     1		                              
0x9d	     	     1	     1		                              
0x9e	     	     1	     1		                              
0x9f	     	     0	     0		EnableAnimationState		                              
0xa0	     	    16	    16		                              
0xaf	     	  1026	  1026		FirmwareUpdate                
0xb0	     	     8	    40	*	UnknownB0                     
0xb2	     	    16	    16		                              
0xb4	     	    21	    21		ObjectMoved                   
0xb5	     	     8	     8		ObjectStoppedMoving           
0xb6	     	    12	    12		ObjectTapped                  
0xb9	     	    10	    10		ObjectTapFiltered             
0xc2	     	     0	     0		RobotDelocalized              
0xc3	     	     0	     0		RobotPoked                    
0xc4	     	     1	     1		AcknowledgeAction            
0xc8	     	    29	    29		                              
0xc9	     	     6	     6		HardwareInfo                  
0xca	     	     1	     1		                              
0xcb	     	     1	     1		                              
0xcd	     	    12	  1036	*	NvStorageOpResult             
0xce	     	     9	     9		ObjectPowerLevel              
0xcf	     	     8	     8		                              
0xd0	     	    13	    13		ObjectConnectionState         
0xd1	     	     3	     3		                              
0xd2	     	    44	    44		                              
0xd7	     	     9	     9		ObjectUpAxisChanged           
0xec	     	     4	     4		                              
0xed	     	    12	    12		BodyInfo                      
0xee	     	   449	   449		FirmwareSignature             
0xef	     	     7	     7		FirmwareUpdateResult          
0xf0	    	    91	    91		RobotState                    
0xf1	    	    15	    15		AnimationState                
0xf2	    	    24	  1172	*	ImageChunk                    
0xf3	    	     9	     9		ObjectAvailable               
0xf4	    	    17	    17		ImageImuData
```


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
