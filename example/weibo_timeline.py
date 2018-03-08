#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/14/18
# @File  : [pachong] weibo_timeline.py

from __future__ import absolute_import
from __future__ import unicode_literals

from crawler import Weibo
from database.mongodb import MongoDB
from fetcher.requests import Requests

project = 'wanghong'
# project = 'test'
# input_ = 'users'
input_ = 'taobaodianzhu'
# fetcher = Requests(proxy="localhost:3128")
fetcher = Requests()
crawler = Weibo(project, input_, fetcher=fetcher, Database=MongoDB) \
    .login('0012028475117', 'Cc19900201')
    # .import_input(input_list=['1866833821'], update=True)
    # .import_input(filepath='profile', update=True)\


# crawler.crawl('profile')
output = 'timeline'
crawler.output = output
crawler.crawl('timeline')
# # self=crawler
# from tqdm import tqdm
# tl = MongoDB('wanghong', 'timeline')
# with tqdm(tl.get_all(), miniters=10000) as bar:
#     for row in bar:
#         mid = row['_id']
#         # likes = row.get('likes', '')
#         # comments = row.get('comments')
#         # forwards = row.get('forwards')
#         # if not likes:
#         #     tl.drop_field(mid, 'likes')
#         # else:
#         #     tl.update(mid, {'likes': int(likes)})
#         # if not comments:
#         #     tl.drop_field(mid, 'comments')
#         # else:
#         #     tl.update(mid, {'comments': int(comments)})
#         # if not forwards:
#         #     tl.drop_field(mid, 'forwards')
#         # else:
#         #     tl.update(mid, {'forwards': int(forwards)})
#         text = row['text'].strip('\u200b \t')
#         tl.update(mid, {'text': text})
#         # urls = row.get('urls', [])
#         # if not urls:
#         #     tl.drop_field(mid, 'urls')
