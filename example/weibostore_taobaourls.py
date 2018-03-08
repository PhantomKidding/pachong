#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/28/18
# @File  : [pachong] weibostore_taobaourls.py


from __future__ import absolute_import
from __future__ import unicode_literals

from crawler import Weibo
from database.mongodb import MongoDB
from fetcher.requests import Requests

project = 'wanghong'
# project = 'test'
input_ = 'users'
fetcher = Requests(proxy='localhost:3128')
crawler = Weibo(project, input_, fetcher=fetcher, Database=MongoDB)

crawler.crawl('shopid')