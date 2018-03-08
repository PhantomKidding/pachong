#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] test.py


from __future__ import unicode_literals
class test(object):
    pass
from database.mongodb import MongoDB


db='pctest'
project = 'wanghong'
task = 'users'
self = MongoDB(db, task)
task in self.conn[db]

collection = task
fields = None
match = {}
for item in self.collection.find(projection= fields): print(item)
self.collection.update({'_id':'1'})
for item in self.input_.collection.find_one({'_id':'2797655824'}): print(item)
print(self.input_.collection.find_one({'_id':'2797655824'})['traceback'])

self.collection.delete_many({'name2': None})
self.collection.update_one({'name': 'huhuhu'}, {'$unset': {'name':None}})
self.collection.insert_many([{'_id': 8, 'name': ['aa', 'bb', 'cc']}, {'_id': 9, 'name': 'ppp'}])
self.update({'_id': 9}, {'name': 'ddd'}, '$push')

self.db['wanghong_timeline_input']
'wanghong_timeline' in set(self.db.collection_names())

self.db['wanghong_timeline'].name

from crawler.weibo import Weibo

for item in self.collection.find({'_id': {'$eq': 4}}): print item
