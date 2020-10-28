
import time

import pycozmo


pycozmo.setup_basic_logging(log_level="DEBUG", protocol_log_level="DEBUG")

conn = pycozmo.conn.Connection(("127.0.0.1", 5551))
conn.start()
conn.connect()

for i in range(100):
    conn.send(pycozmo.protocol_encoder.SetRobotVolume(i))

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

conn.disconnect()
conn.stop()
