#!/usr/bin/env python

import sys
import time

import dpkt

import pycozmo


def load_engine_pkts(fspec):
    pkts = []

    frame_count = 1
    with open(fspec, "rb") as f:
        first_ts = None
        for ts, frame in dpkt.pcap.Reader(f):
            if first_ts is None:
                first_ts = ts
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
            frame = pycozmo.Frame.from_bytes(udp.data)
            if frame.type not in [pycozmo.protocol_declaration.FrameType.ENGINE]:
                # Skip non-engine frames
                continue
            for pkt in frame.pkts:
                if pkt.type not in [pycozmo.protocol_declaration.PacketType.COMMAND,
                                    pycozmo.protocol_declaration.PacketType.UNKNOWN_0A]:
                    continue
                pkts.append(pkt)
            frame_count += 1

    print("Loaded {} engine packets.".format(len(pkts)))

    return pkts


def replay(fspec):
    pkts = load_engine_pkts(fspec)

    pycozmo.setup_basic_logging(log_level="DEBUG", protocol_log_level="DEBUG")
    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    for i, pkt in enumerate(pkts):
        input()
        print("{}".format(i))
        cli.send(pkt)

    cli.disconnect()
    time.sleep(1)


def main():
    replay(sys.argv[1])


if __name__ == '__main__':
    main()
