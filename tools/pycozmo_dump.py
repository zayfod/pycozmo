#!/usr/bin/env python

import sys
import os
import dpkt
try:
    # noinspection PyPackageRequirements
    import pcap
except ImportError:
    pcap = None

import pycozmo


packet_count = 0
unknown_count = 0
frame_count = 1
first_ts = None


def decode_cozmo_frame(ts, buffer):
    global packet_count
    global unknown_count

    frame = pycozmo.Frame.from_bytes(buffer)

    # if frame.type == pycozmo.protocol_declaration.FrameType.PING:
    #     return

    print("{:<12s}first_seq={:04x}, seq={:04x}, ack={:04x}, frame={:6d}, time={:.06f}".format(
        frame.type.name, frame.first_seq, frame.seq, frame.ack, frame_count, ts))

    for pkt in frame.pkts:
        packet_count += 1
        if isinstance(pkt, pycozmo.protocol_base.UnknownPacket):
            unknown_count += 1
        # if isinstance(pkt, pycozmo.protocol_encoder.Ping):
        #     continue
        print("\t{:<12s} time={:.06f} {}".format(frame.type.name, ts, pkt))
        # if ts > 15:
        #     sys.exit(1)


def handle_frame(ts, frame):
    global frame_count
    global first_ts

    if first_ts is None:
        first_ts = ts
    rel_ts = ts - first_ts
    eth = dpkt.ethernet.Ethernet(frame)
    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
        # Skip non-IP frames
        return
    ip = eth.data
    if ip.p != dpkt.ip.IP_PROTO_UDP:
        # Skip non-UDP frames
        return
    udp = ip.data
    if udp.data[:7] != pycozmo.protocol_declaration.FRAME_ID:
        # Skip non-Cozmo frames
        return
    decode_cozmo_frame(rel_ts, udp.data)
    frame_count += 1
    # if frame_count > 100:
    #     break


def decode_pcap(fspec):
    with open(fspec, "rb") as f:
        for ts, frame in dpkt.pcap.Reader(f):
            handle_frame(ts, frame)

    print()
    print("Frames: {}".format(frame_count))
    print("Packets: {}".format(packet_count))
    if packet_count:
        print("Unknown packets: {} ({:.0f}%)".format(unknown_count, 100.0*unknown_count/packet_count))


def capture(interface):
    if pcap is None:
        sys.exit("Live packet capturing requires pypcap. Install with 'pip install pypcap'.")

    pc = pcap.pcap(name=interface)
    # pc.setfilter('')
    print('listening on %s: %s' % (pc.name, pc.filter))
    pc.loop(0, handle_frame)


def main():
    fspec = sys.argv[1]
    if os.path.exists(fspec):
        decode_pcap(fspec)
    else:
        capture(fspec)


if __name__ == '__main__':
    main()
