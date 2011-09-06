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

#random segment array
segment = []
for n in range(0, 9):
    segment.append({'x' : float(random.random()), 'y' : float(random.random()), 'z' : float(random.random())})

segment_id = pebble.session.track_segment("123", segment, int(time.time()), int(time.time()))
print(segment_id)

pebble.session.stop()
print(pebble.session)
