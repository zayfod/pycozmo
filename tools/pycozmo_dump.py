#!/usr/bin/env python

import sys
import dpkt

import pycozmo


def decode_cozmo_frame(frame_count, ts, buffer):
    frame = pycozmo.Frame.from_bytes(buffer)

    print("{:<12s}first_seq={:04x}, seq={:04x}, ack={:04x}, frame={:6d}, time={:.06f}".format(
        frame.type.name, frame.first_seq, frame.seq, frame.ack, frame_count, ts))

    for pkt in frame.pkts:
        print("\t{}".format(pkt))


def decode_pcap(fspec):
    frame_count = 1
    with open(fspec, "rb") as f:
        first_ts = None
        for ts, frame in dpkt.pcap.Reader(f):
            if first_ts is None:
                first_ts = ts
            rel_ts = ts - first_ts
            eth = dpkt.ethernet.Ethernet(frame)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                # Skip non-IP frames
                continue
            ip = eth.data
            if ip.p != dpkt.ip.IP_PROTO_UDP:
                # Skip non-UDP frames
                continue
            udp = ip.data
            if udp.data[:7] != pycozmo.protocol_declaration.FRAME_ID:
                # Skip non-Cozmo frames
                continue
            decode_cozmo_frame(frame_count, rel_ts, udp.data)
            frame_count += 1
            # if frame_count > 100:
            #     break


def main():
    decode_pcap(sys.argv[1])


if __name__ == '__main__':
    main()
