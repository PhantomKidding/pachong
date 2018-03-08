#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/16/18
# @File  : [pachong] example_mongodb.py


from database import MongoDB

db = MongoDB('wanghong', 'users')
print(db.find('2045908335')['weibos'])
db2 = MongoDB('wanghong', 'users_full')

current_ids = {doc['_id'] for doc in db2.find_all({})}
for doc in db.find_all({}):
    if doc['_id'] in current_ids:
        db2.update(doc['_id'], doc)
    else:
        db2.insert(doc)


n_followers = [doc.get('n_followers', 0) for doc in db2.find_all({})]
import pandas
tar = pandas.DataFrame(n_followers)
tar.describe()


MongoDB('wanghong', 'taobao_items').update('559774227824', a)

for item in db2.find_all({'$nor': [{'winfo': {'$regex': '(品牌主理人|工作室创始人)'}},
                                  {'pinfo': {'$regex': '(品牌主理人|工作室创始人)'}}]}):
    db2.drop(item['_id'])

for item in db2.find_all({'$and': [{'n_followers': {'$gte': 338}},
                                   {'n_weibos': {'$gte': 40}}]}):
    db.insert(item)

for item in db.find_all({'task.shopid.status': 'error'},['task.shopid.traceback']):
    print item


a = db.get({'task.timeline.status': 'error'})
print(a['task']['timeline']['traceback'])
test = MongoDB('test', 'user')
for item in test.get_all(): print(item)
test.insert({'_id': 1, 'test': [('h额呵呵', 1), ('啊哈哈哈', 'http')]})
a = test.get(1)
for item in a['test']:
    print(item[0])
    print(item[1])



import pymongo
from sshtunnel import SSHTunnelForwarder

MONGO_HOST = "10.0.1.29"
MONGO_PORT = 27017
MONGO_DB = "test"
MONGO_USER = "cchen"
MONGO_PASS = "Cc19900201"

db = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db['test']['test'].insert({'b': 'haha'})
a = db['test']['test'].find()
from tqdm import tqdm
with tqdm(a, total=a.count()) as bar:
    for b in bar:
        print(b)
a.count()

a=a.skip(1)
a.next()

db['test']['test'].update_one({'b':'haha'}, {'$set': {'d': 'hehe'}})

server = SSHTunnelForwarder(
    MONGO_HOST,
    remote_bind_address=('127.0.0.1', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
db['test'].insert({'a': 'haha'})

server.stop()


db = MongoDB('wanghong', 'taobao_items')
ids = [doc['_id'] for doc in db.find_all({'task.itempage.status': {'$ne': 'done'}})]
ids = ids[-10000:]

for x in range(10000):
    if x % 1000 == 0:
        f = open('itemids{}.txt'.format(x/1000), 'w')
    f.write(ids[x] + '\n')