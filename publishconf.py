#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# Copyright (c) 2020 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://pbarker.dev'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
