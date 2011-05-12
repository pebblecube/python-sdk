API_KEY = "qwe"
API_SECRET = "qwe"

import sys
sys.path.append("../src")
import pebblecube
import pprint

pebble = pebblecube.PebblecubeApi("0617bcfcadf6fa6bd0a50390135b527204dba63cb", "56a86878a0e5b05ee405d6d01f8c7fbf04dba63cb")

pebble.session.start()
print(pebble.session)

pebble.session.stop()
print(pebble.session)
