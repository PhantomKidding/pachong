#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] exceptions.py


from __future__ import unicode_literals


class PachongException(BaseException):

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return {'status': self.status, 'message': self.message}


class TargetNotFoundError(PachongException):
    def __init__(self, message='The target is not found or not matched.'):
        self.status = 404
        self.message = message
