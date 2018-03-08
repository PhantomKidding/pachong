#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] base.py


import warnings


class Database(object):

    def insert(self, document):
        raise NotImplementedError

    def insert_many(self, documents):
        raise NotImplementedError

    def find(self, match, fields=None):
        raise NotImplementedError

    def find_all(self, match, fields=None):
        raise NotImplementedError

    def drop(self, match):
        raise NotImplementedError

    def update(self, match, document, method='$set'):
        raise NotImplementedError

    def import_input(self, filepath):
        raise NotImplementedError
