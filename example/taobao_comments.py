#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 3/6/18
# @File  : [pachong] taobao_comments.py


from __future__ import absolute_import
from __future__ import unicode_literals

from crawler.taobao import Taobao
from database.mongodb import MongoDB
from fetcher.requests import Requests

fetcher = Requests(proxy='localhost:3129')
# fetcher = Browser(proxy='13.56.211.230:3128')
crawler = Taobao('wanghong', 'taobao_items', output='taobao_comments', fetcher=fetcher, Database=MongoDB)
crawler.profile = 'taobao_shops'
crawler.ua = '098#E1hvQvvUvbpvUvCkvvvvvjiPPFsp1jDRPLs9ljnEPmPZ1jlHPsFZgjiURLsWljlRiQhvCvvv9UUPvpvhvv2MMQyCvhQhNNyvC0RvQRAn+byDCaLIAXZTKFEw9ExrQ8Tx46JDYRLhVBi+Vd0DyOvO5onmsX7v0C6tExjxAfev+XgqBdmxfJmK5eUySweU+b8ruphvmvvv9bmMHlGSkphvC99vvOH0pdyCvm9vvvvWphvv2vvv9xtvpv17vvv2ohCvhV9vvvnUphvW9Qvvv63vpv1MvphvC9vhvvCvp2yCvvpvvvvv'
crawler.crawl('comments')
