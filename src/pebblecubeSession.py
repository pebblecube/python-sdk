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
import pebblecube

class PebblecubeSession:
    sessionId = None
    startedAt = None
    elapsedTime = None
    stoppedAt = None
    pebble = None

    def __init__(self, pebble):
        self.data = []
        self.pebble = pebble

    def __repr__(self):
        return "<session sessionId:%s startedAt:%s elapsedTime:%s stoppedAt:%s>" % (self.sessionId, self.startedAt, self.elapsedTime, self.stoppedAt)

    def start(self, params = None):
        result = self.pebble.request("/sessions/start", "GET", None)
        if result:
            self.sessionId = result["k"]
            self.startedAt = result["t"]
        else:
           raise pebblecube.PebblecubeException("invalid session")

    def stop(self):
        if self.sessionId:
            result = self.pebble.request("/sessions/stop", "GET", {"session_key" : str(self.sessionId)})
            if result:
                self.elapsedTime = result["t"]
                self.stoppedAt = int(self.startedAt) + int(self.elapsedTime)
        else:
           raise pebblecube.PebblecubeException("session not started")
