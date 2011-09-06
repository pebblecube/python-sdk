API_KEY = "YOUR_KEY"
API_SECRET = "YOUR_SECRET"

import sys
sys.path.append("../src")
import pebblecube
import pprint
import random
import time

pebble = pebblecube.PebblecubeApi(API_KEY, API_SECRET)

pebble.session.start()
print(pebble.session)

event = [{'code':'test_string', 'value':str(random.random()), 'time':int(time.time())},{'code':'test_float', 'value':float(random.random()), 'time':int(time.time())}]

server_time = pebble.session.send_event(event)
print(server_time)

pebble.session.stop()
print(pebble.session)
