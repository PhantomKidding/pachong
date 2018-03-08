#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 3/3/18
# @File  : [pachong] taobao_itemlist.py



from __future__ import absolute_import
from __future__ import unicode_literals

from crawler.taobao import Taobao
from database.mongodb import MongoDB
from fetcher.selenium import Browser

fetcher = Browser(proxy='localhost:3128')
# fetcher = Browser(proxy='13.56.211.230:3128')
crawler = Taobao('wanghong', 'taobao_shops', output='taobao_items', fetcher=fetcher, Database=MongoDB) \
    .set_pushbullet('o.cJm1iLu3sJtvm7P0YIHuBvy8lpYtPOIQ') \
    .login()

crawler.crawl('itemlist')
