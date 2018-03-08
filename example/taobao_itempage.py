#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 3/6/18
# @File  : [pachong] taobao_itempage.py


from __future__ import absolute_import
from __future__ import unicode_literals

from crawler.taobao import Taobao
from database.mongodb import MongoDB
from fetcher.selenium import Browser
import sys


args = sys.argv[1:]
nfile = int(args[0])

# fetcher = Browser(proxy='localhost:3128')
fetcher = Browser()
# fetcher = Browser(proxy='13.56.211.230:3128')
crawler = Taobao('wanghong', 'taobao_items', fetcher=fetcher, Database=MongoDB).import_input('itemids{}.txt'.format(nfile))
    # .login()

crawler.crawl('itempage')