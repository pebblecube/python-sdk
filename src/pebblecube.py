#!/usr/bin/env python
#
# Copyright 2011 Pebblecube
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import urllib
import hashlib
import pebblecubeSession
import json

json_parser = lambda s: json.loads(s)

class PebblecubeApi(object):
        api_key = ""
        api_secret = ""
        api_sig = ""
        server_url = ""
        session = None
	
	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret
		self.server_url = "https://api.pebblecube.com"
		self.api_sig = hashlib.md5(api_key+api_secret).hexdigest()
		self.session = pebblecubeSession.PebblecubeSession(self)

        def request(self, url, method = 'GET', params = None):
                if not params: params = {}
                params["api_sig"] = self.api_sig;
                params["api_key"] = self.api_key;
                #get
                file = urllib.urlopen(self.server_url + url + "?" + urllib.urlencode(params))
                #parse response
                try:
                        response = json_parser(file.read())
                        if file.code >= 400:
                                raise PebblecubeException(response["e"])
                finally:
                        file.close()
                #return
                return response

class PebblecubeException(Exception):
        def __init__(self, message):
                Exception.__init__(self, message)
