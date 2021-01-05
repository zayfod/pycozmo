#!/user/env python

import time
import pycozmo

with pycozmo.connect(log_level="DEBUG",protocol_log_level="DEBUG",enable_animations=False) as cli:
     while True:
         time.sleep(0.1)
