#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# Copyright (c) 2020 Paul Barker <paul@pbarker.dev>
# SPDX-License-Identifier: Apache-2.0

from __future__ import unicode_literals
from pelican import __version__ as PELICAN_VERSION

AUTHOR = 'Paul Barker'
COPYRIGHT_YEAR = '2020-2023'
SITENAME = 'Paul Barker'
SITEURL = ''
THEME = 'theme'

PATH = 'content'
ARTICLES_PATHS = ('posts', )
PAGE_PATHS = ('pages', )

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

OUTPUT_PATH = 'public'

FEED_ALL_ATOM = 'feed.atom'
FEED_ALL_RSS = 'feed.rss'
TAG_FEED_ATOM = 'tags/{slug}/feed.atom'
TAG_FEED_RSS = 'tags/{slug}/feed.rss'
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TAG_SAVE_AS = 'tags/{slug}/index.html'
TAG_URL = 'tags/{slug}/'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'

MENUITEMS = (
    ('Tags', '/tags/'),
)

DEFAULT_PAGINATION = 10

PLUGINS = (
    'neighbors',
    'pelican_youtube',
)

STATIC_PATHS = (
    'css',
    'images',
    'pgpkeys.asc',
    'sshkeys.txt',
    'sshkeys.txt.asc'
)

ARTICLE_URL = 'posts/{date:%Y-%m-%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y-%m-%d}/{slug}/index.html'

ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
