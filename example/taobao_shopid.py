#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 3/1/18
# @File  : [pachong] taobao_shopid.py


from __future__ import absolute_import
from __future__ import unicode_literals

from crawler.taobao import Taobao
from database.mongodb import MongoDB
from fetcher.requests import Requests

project = 'wanghong'
# project = 'test'
input_ = 'users'
fetcher = Requests(proxy='localhost:3128')
crawler = Taobao(project, input_, fetcher=fetcher, Database=MongoDB)
    # .import_input(input_list=['1866833821'], update=True)
    # .import_input(filepath='profile', update=True)\

crawler.crawl('shopid2')