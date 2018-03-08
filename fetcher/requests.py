#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/14/18
# @File  : [pachong] requests.py

from __future__ import absolute_import

import json
import random
import time

from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

from crawler.common.timeout import timeout
from .base import Fetcher


class Requests(Fetcher):
    MAX_RETRIES = 9
    STATUS_FORCELIST = [500]

    def __init__(self, session=None, proxy=None):
        self.session = session
        self.proxy = proxy

    @timeout(30)
    def get(self, url, **kwargs):
        self.response = self.session.get(url, **kwargs)
        soup = BeautifulSoup(self.response.content, 'lxml')
        if kwargs.get('overwrite', True) is False:
            return soup
        self.soup = soup
        time.sleep(5 + random.random() * 5)
        return True

    def get_json(self, url, **kwargs):
        html = self.session.get(url, **kwargs)
        data = json.loads(html.content)
        return data

    def find(self, *args, **kwargs):
        return self.soup.find(*args, **kwargs)

    def find_all(self, *args, **kwargs):
        return self.soup.find_all(*args, **kwargs)

    def source_code(self):
        return self.soup.prettify()

    def build(self, source_page, builder='lxml', overwrite=True):
        _soup = BeautifulSoup(source_page, builder)
        if overwrite:
            self.soup = _soup
            return self
        else:
            return _soup

    def save(self, fp_out):
        with open(fp_out, 'w') as o:
            o.write(self.source_code())

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, val):
        self._proxy = val
        self._session.proxies.update({'http': self.proxy, 'https': self.proxy})

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, val):
        if val:
            self._session = val
        else:
            self._session = Session()
            retries = Retry(total=self.MAX_RETRIES, status_forcelist=self.STATUS_FORCELIST)
            self._session.mount('https://', HTTPAdapter(max_retries=retries))
            if self.proxy:
                self._session.proxies \
                    .update({'http': self.proxy, 'https': self.proxy})
            self._session.headers \
                .update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                                       '(KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
