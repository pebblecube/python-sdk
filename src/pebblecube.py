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
import urllib2
import hashlib
import pebblecubeSession
import pebblecubeCrypt
import json
import os
import base64

json_parser = lambda s: json.loads(s)

class PebblecubeApi(object):
        api_key = ""
        api_secret = ""
        api_sig = ""
        server_url = ""
        session = None
        cipher = None
	
	def __init__(self, api_key, api_secret, cipher = None):
		self.api_key = api_key
		self.api_secret = api_secret
		self.server_url = "https://api.pebblecube.com"
		self.api_sig = hashlib.md5(api_key+api_secret).hexdigest()
		self.session = pebblecubeSession.PebblecubeSession(self)
		self.cipher = cipher

        def request(self, url, method = 'GET', parameters = None):
                params = {}

                iv = None
                if self.cipher:
                        iv = os.urandom(16)
                        if parameters:
                                #encryption required
                                params["data"] = self.encrypt(urllib.urlencode(parameters), iv)
                else:
                        params = parameters
                        
                params["api_sig"] = self.api_sig;
                params["api_key"] = self.api_key;

                #switch on the method
                if method == "POST":
                        req = urllib2.Request(self.server_url + url, urllib.urlencode(params))
                        if iv:
                                req.add_header('PC_IV', base64.b64encode(iv))
                        file = urllib2.urlopen(req)
                else:
                        opener = urllib2.build_opener()
                        
                        if iv:
                                opener.addheaders = [('PC_IV', base64.b64encode(iv))]
                                
                        file = opener.open(self.server_url + url + "?" + urllib.urlencode(params))                        

                #parse response
                try:
                        head = file.info()
                        response_iv = None
                        
                        if 'PC_IV' in head:
                                response_iv = head["PC_IV"]
                                
                        response = json_parser(self.decrypt(file.read(), response_iv))
                        
                        if file.code >= 400:
                                raise PebblecubeException(response["e"])
                finally:
                        file.close()

                #return
                return response
        
        def encrypt(self, text, iv):
                """Encrypts a string using aes, mode of operation cbc.

                arguments:
                text -- text to encrypt
		iv -- Initialition vector
                """
                if self.cipher:

                        if self.cipher == "256":
                                BLOCK_SIZE = 32
                        elif self.cipher == "192":
                                BLOCK_SIZE = 24
                        else:
                                BLOCK_SIZE = 16
                        
                        KEY = self.api_secret[0:BLOCK_SIZE]
                        e = pebblecubeCrypt.encryptor(KEY, iv)
                        return e(text)
                else:
                        return text

        def decrypt(self, text, iv):
                """Decrypts a base64 string using aes, mode of operation cbc.

                arguments:
                text -- base64 encrypted content to decrypt
		iv -- Initialition vector
                """
                if self.cipher:
                        if self.cipher == "256":
                                BLOCK_SIZE = 32
                        elif self.cipher == "192":
                                BLOCK_SIZE = 24
                        else:
                                BLOCK_SIZE = 16
                        
                        KEY = self.api_secret[0:BLOCK_SIZE]
                        d = pebblecubeCrypt.decryptor(KEY, iv)
                        return d(text)
                else:
                        return text


class PebblecubeException(Exception):
        def __init__(self, message):
                Exception.__init__(self, message)
