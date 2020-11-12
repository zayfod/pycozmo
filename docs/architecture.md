
PyCozmo Architecture
====================


Overview
--------

PyCozmo is designed as a multithreaded library.

It is organized in three layers with each higher layer building on the ones below it: 
- low-level connection layer
- client or SDK layer
- application layer

Each layer provides it's own API and can be used independently.

The following diagram illustrates the library architecture.

```
                                                                             ^
                                                                             |
                    +-----------------------------------------+              |
                    |                                         |              |
                    |                  Brain                  |              |
                    |                                         |              |
                    |                                         |              |
                    +-----+--------------+--------------+-----+              |
                          ^              |              ^                    |
                          |              |              |                    |
     +-----------+  +-----+-----+        |              |                    |  Application
     |           |  |           |        |              |                    |  Layer
     | Heartbeat |  |  Reaction |        |              |                    |
     |  Thread   |  |   Thread  |        |              |                    |
     |           |  |           |        |              |                    |
     +-----+-----+  +-----+-----+        |              |                    |
           |              ^              |  Commands    |  Events            |
           |              |              |              |                    |
           |             +-+             |              |                    |
           |             |-|  Event      |              |                    |
           |             |-|  Queue      |              |                    |
           |             +-+             |              |                    |
           |              ^              |              |                    |
           |              |              |              |                    v
           +------------->+  Reactions   |              |
                          |              v              |                    ^
                    +-----+--------------+--------------+-----+              |
                    |                                         |              |
                    |                  Client                 |              |
                    |                                         |              |
                    |                                         |              |
                    +-----+--------------+--------------+-----+              |
                          |              |              ^                    |  SDK
                          v              |              |                    |  Layer
                         +-+             |              |                    |
              Animation  |-|             |  Commands    |  Events            |
                Queue    |-|             |              |                    |
                         +-+             |              |                    |
                          |              |              |                    |
                          v              v              |                    |
+-----------+       +-----+-----+  +-----+--------------+-----+              |
|           |       |           |  |                          |              |
|   Face    |       | Animation |  |        Connection        |              v
| Generator +------>+  Thread   |  |          Thread          |
|           |       |           |  |                          |              ^
+-----------+       +-----+-----+  +-----+--------------+-----+              |
                          |              |              ^                    |
                          +------------->+              |                    |
                                         |              |                    |
                                         v              |                    |
                                        +-+            +-+                   |
                              Outgoing  |-|            |-|  Incoming         |
                               Message  |-|            |-|   Message         |
                                Queue   +-+            +-+    Queue          |
                                         |              ^                    |
                                         v              |                    |  Connection
                                   +-----+-----+  +-----+-----+              |  Layer
                                   |           |  |           |              |
                                   |   Send    |  |  Receive  |              |
                                   |  Thread   |  |  Thread   |              |
                                   |           |  |           |              |
                                   +---------+-+  +--+--------+              |
                                             |       ^                       |
                                             |       |                       |
                                             |       |                       |
                                             v       |                       |
                                           +-+-------+-+                     |
                                           |           |                     |
                                           |    UDP    |                     |
                                           |   Socket  |                     |
                                           |           |                     |
                                           +-----------+                     |
                                                                             v
```

Connection Layer
----------------

The connection layer implements the Cozmo communication protocol.

The receive thread reads Cozmo protocol frames, encapsulated in UDP datagrams, from the UDP socket. It maintains
a receive window for incoming packets and sends a stream of incoming packets in the correct order over the incoming
message queue to the connection thread.

The send thread reads a stream of outgoing packets from the outgoing message queue, builds Cozmo protocol frames
and sends them over the UDP socket. It maintains a send window and resends packets that are not acknowledged in time.

The connection thread reads a stream of incoming packets from the incoming message queue and dispatches them to
registered handler functions. It sends ping packets on a regular basis to maintain connection with the robot. 


Client Layer (SDK)
------------------

The client layer provides access to robot on-board functions.

It allows sending commands and registering handler function for incoming packets and events.

It performs:
- camera image reconstruction
- display image encoding
- audio encoding
- animation and audio playback
- procedural face generation 

The animation controller synchronizes animations, audio playback, and image display. It works as a separate thread
that aims to send images and audio to the robot at 30 frames per second. All on-board function of the robot are
synchronized to this framerate, including images, audio playback, backpack and cube LED animations.


Application Layer
-----------------

The application layer implements high-level off-board functions:
- reactions and behaviors
- personality engine
- computer vision (CV) camera image processing

Events from the client layer are converted to reactions. The reaction thread reads events from its incoming event
queue and handles them appropriately. Reactions normally trigger behaviors.

The heartbeat thread drives the personality engine and timers for activities and behaviors.
