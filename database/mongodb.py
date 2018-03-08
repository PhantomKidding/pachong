#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] mongodb.py

from __future__ import absolute_import

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from database.base import Database


class MongoDB(Database):

    def __init__(self, db='', collection=''):
        self.db_name = db
        self.collection_name = collection
        if db:
            self.conn = MongoClient()
            self.db = self.conn[db]
        if collection:
            self.collection = self.db[collection]

    def insert(self, document):
        document = document if isinstance(document, dict) else {'_id': document}
        try:
            self.collection.insert_one(document)
        except DuplicateKeyError:
            pass

    def insert_many(self, documents):
        documents = documents if isinstance(documents[0], dict) else [{'_id': doc} for doc in documents]
        [self.collection.insert(document) for document in documents]

    def find(self, match, fields=None):
        match = match if isinstance(match, dict) else {'_id': match}
        return self.collection.find_one(match, fields)

    def find_all(self, match=None, fields=None):
        match = match if isinstance(match, dict) else {'_id': match}
        return self.collection.find(match, fields)

    def drop(self, match):
        match = match if isinstance(match, dict) else {'_id': match}
        return self.collection.delete_many(match)

    def drop_field(self, match, field):
        match = match if isinstance(match, dict) else {'_id': match}
        return self.collection.update_one(match, {'$unset': {field: None}})

    def drop_field_all(self, field):
        return [self.drop_field(doc['_id'], field)
                for doc in self.find_all(fields=['_id'])]

    def update(self, match, document, method='$set'):
        match = match if isinstance(match, dict) else {'_id': match}
        return self.collection.update_one(match, {method: document})

