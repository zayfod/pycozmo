
def hex_dump(data: bytes) -> str:
    res = ":".join("{:02x}".format(b) for b in data)
    return res
