#!/usr/bin/env python

from threading import Event

import pycozmo


e = Event()


def on_nv_storage_op_result(cli: pycozmo.client.Client, pkt: pycozmo.protocol_encoder.NvStorageOpResult):
    print(pkt.result)
    print(pkt.data)
    if pkt.result != pycozmo.protocol_encoder.NvResult.NV_MORE:
        e.set()


with pycozmo.connect(enable_animations=False, log_level="DEBUG") as cli:

    cli.add_handler(pycozmo.protocol_encoder.NvStorageOpResult, on_nv_storage_op_result)

    pkt = pycozmo.protocol_encoder.NvStorageOp(
        tag=pycozmo.protocol_encoder.NvEntryTag.NVEntry_CameraCalib,
        length=1,
        op=pycozmo.protocol_encoder.NvOperation.NVOP_READ)
    cli.conn.send(pkt)

    e.wait(timeout=20.0)
