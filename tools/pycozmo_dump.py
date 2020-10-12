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


class DumpApp(object):

    def __init__(self):
        self.first_ts = None
        self.frame_count = 0
        self.filtered_frame_count = 0
        self.packet_count = 0
        self.unknown_count = 0
        self.filtered_packet_count = 0
        self.frame_type_filter = pycozmo.filter.Filter()
        # self.frame_type_filter.deny_ids({pycozmo.protocol_declaration.FrameType.PING.value})
        self.packet_type_filter = pycozmo.filter.Filter()
        # self.packet_type_filter.deny_ids({pycozmo.protocol_declaration.PacketType.PING.value})
        self.packet_id_filter = pycozmo.filter.Filter()
        # self.packet_id_filter.deny_ids({0x8f, 0x97})

    def decode_cozmo_frame(self, ts, buffer):
        frame = pycozmo.Frame.from_bytes(buffer)

        if self.frame_type_filter.filter(frame.type.value):
            self.filtered_frame_count += 1
            return

        print("{:<12s}first_seq=0x{:04x}, seq=0x{:04x}, ack=0x{:04x}, frame={:6d}, time={:.06f}".format(
            frame.type.name, frame.first_seq, frame.seq, frame.ack, self.frame_count + 1, ts))

        for pkt in frame.pkts:
            self.packet_count += 1
            if isinstance(pkt, pycozmo.protocol_base.UnknownPacket):
                self.unknown_count += 1
            if self.packet_type_filter.filter(pkt.type.value):
                self.filtered_packet_count += 1
                continue
            if self.packet_id_filter.filter(pkt.id):
                self.filtered_packet_count += 1
                continue
            direction = "->" if pkt.is_from_robot() else "<-"
            print("\t{} time={:.06f} {}".format(direction, ts, pkt))
            # if ts > 15:
            #     sys.exit(1)

    def handle_frame(self, ts, frame):
        if self.first_ts is None:
            self.first_ts = ts
        rel_ts = ts - self.first_ts
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
        self.decode_cozmo_frame(rel_ts, udp.data)
        self.frame_count += 1
        # if frame_count > 100:
        #     break

    def decode_pcap(self, fspec):
        with open(fspec, "rb") as f:
            for ts, frame in dpkt.pcap.Reader(f):
                self.handle_frame(ts, frame)

        print()
        print("Frames: {}".format(self.frame_count))
        print("Packets: {}".format(self.packet_count))
        if self.packet_count:
            print("Unknown packets: {} ({:.0f}%)".format(
                self.unknown_count, 100.0*self.unknown_count/self.packet_count))

    def capture(self, interface):
        pc = pcap.pcap(name=interface)
        # pc.setfilter('')
        print('listening on %s: %s' % (pc.name, pc.filter))
        pc.loop(0, self.handle_frame)


def main():
    fspec = sys.argv[1]

    app = DumpApp()

    if os.path.exists(fspec):
        app.decode_pcap(fspec)
    else:
        if pcap is None:
            sys.exit("Live packet capturing requires pypcap. Install with 'pip install --user pypcap'.")

        app.capture(fspec)


if __name__ == '__main__':
    main()
