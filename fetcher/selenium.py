#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/27/18
# @File  : [pachong] selenium.py


from __future__ import absolute_import
from __future__ import unicode_literals

import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from six import iteritems
from six.moves.urllib.parse import urlencode
import time
import random

from .base import Fetcher


class Browser(Fetcher):
    MAX_RETRIES = 9
    MAX_WAITTIME = 30
    STATUS_FORCELIST = [500]

    def __init__(self, session=None, proxy=None):
        self.proxy = proxy
        self.session = session

    def get(self, url, **kwargs):
        params = kwargs.get('params')
        if params:
            delimiter = kwargs.get('delimiter', '?')
            url += delimiter + urlencode(params)
        until = kwargs.get('until')
        until_not = kwargs.get('until_not')

        for x in range(self.MAX_RETRIES + 1):
            try:
                self.session.get(url)
                time.sleep(5 + random.random() * 5)
                if until:
                    uu = self.wait_until(until)
                    return uu if uu else self.get(url, **kwargs)
                if until_not:
                    un = self.wait_until_not(until_not)
                    return un if un else self.get(url, **kwargs)
                return True
            except TimeoutException:
                continue
        raise TimeoutException

    # def get_json(self, url, **kwargs):
    #     html = self.session.get(url, **kwargs)
    #     data = json.loads(html.content)
    #     return data

    def find(self, *args, **kwargs):
        try:
            if 'xpath' in kwargs:
                return self.session.find_element_by_xpath(kwargs['xpath'])
            if len(args) == 2:
                kwargs = args[1]
            if 'class_' in kwargs:
                kwargs['class'] = kwargs['class_']
                kwargs.pop('class_')
            xpath = '//' + args[0]
            if kwargs:
                xpath += '[' + \
                         ' and '.join(
                             'contains({}, "{}")'.format('text()' if k == 'text' else '@' + k, v.pattern)
                             if isinstance(v, re._pattern_type) else
                             '@{}="{}"'.format(k, v)
                             for k, v in iteritems(kwargs)
                         ) + \
                         ']'
            return self.session.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None

    def find_all(self, *args, **kwargs):
        if 'xpath' in kwargs:
            return self.session.find_elements_by_xpath(kwargs['xpath'])
        if len(args) == 2:
            kwargs = args[1]
        if 'class_' in kwargs:
            kwargs['class'] = kwargs['class_']
            kwargs.pop('class_')
        xpath = '//' + args[0] + '[' + ' and '.join('@{}="{}"'.format(k, v) for k, v in iteritems(kwargs)) + ']'
        return self.session.find_elements_by_xpath(xpath)

    def source_code(self):
        return self.session.page_source

    def save(self, fp_out):
        with open(fp_out, 'w') as o:
            o.write(self.source_code())

    def wait_until(self, until):
        if until and not callable(until):
            raise TypeError('until must be a function.')
        try:
            return WebDriverWait(self.session, self.MAX_WAITTIME).until(until)
        except TimeoutException:
            return None

    def wait_until_not(self, until_not):
        if until_not and not callable(until_not):
            raise TypeError('until_not must be a function.')
        try:
            return WebDriverWait(self.session, self.MAX_WAITTIME).until_not(until_not)
        except TimeoutException:
            return None

    def move_to(self, ele):
        actions = ActionChains(self.session)
        actions.move_to_element(ele)
        actions.perform()
        time.sleep(1)

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, val):
        if val:
            self._session = val
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            if self.proxy:
                chrome_options.add_argument('--proxy-server=%s' % self.proxy)
            self._session = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
