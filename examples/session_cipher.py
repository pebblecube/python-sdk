API_KEY = "YOUR_KEY"
API_SECRET = "API_SECRET"

import sys
sys.path.append("../src")
import pebblecube
import pprint

pebble = pebblecube.PebblecubeApi(API_KEY, API_SECRET, "256")

pebble.session.start()
print(pebble.session)

pebble.session.stop()
print(pebble.session)
