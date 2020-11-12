
import time

import pycozmo


pycozmo.setup_basic_logging(log_level="DEBUG", protocol_log_level="DEBUG")

conn = pycozmo.conn.Connection(server=True)
conn.start()

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

conn.stop()
