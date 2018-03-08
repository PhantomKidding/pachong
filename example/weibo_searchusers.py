#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/28/18
# @File  : [pachong] weibo_searchusers.py


from __future__ import absolute_import
from __future__ import unicode_literals

from crawler import Weibo
from database.mongodb import MongoDB
from fetcher.selenium import Browser


fetcher = Browser()
crawler = Weibo('wanghong', 'searchkeywords2', output='taobaodianzhu', fetcher=fetcher, Database=MongoDB)\
    .import_input(input_list=['淘宝店主']) \
    .login('0012028475117', 'Cc19900201')

crawler.crawl('searchusers')