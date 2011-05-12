#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
	name = 'pebblecube-python-sdk',
	version = '0.1',
	description = 'Python SDK for the Pebblecube APIs',
	author = 'Pebblecube',
	url = 'http://github.com/pebblecube/python-sdk',
	package_dir = { '' : 'src' },
	py_modules = [
		'pebblecube',
		]
)