#!/usr/bin/env python
# coding=utf-8
"""This is the entry point when the puls module is executed (not imported!).
This is the preferred way of starting up the development server:

python puls

This file is IGNORED when running the deployment version, as uWSGI just imports
the puls module, and makes no attempt to execute this file.
"""
from __future__ import absolute_import, unicode_literals, division


# fix import path
import sys
import os
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.getcwd())

# load module and run it in debug mode
import puls
puls.app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
