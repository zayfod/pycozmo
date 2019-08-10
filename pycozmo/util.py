
def hex_dump(data: bytes) -> str:
    res = ":".join("{:02x}".format(b) for b in data)
    return res


def hex_load(data: str) -> bytes:
    res = bytearray.fromhex(data.replace(":", ""))
    return res


def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step
