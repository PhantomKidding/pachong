#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 3/7/18
# @File  : [pachong] valid.py


import requests
import time
from requests.exceptions import ProxyError, ConnectionError, SSLError, ReadTimeout, ConnectTimeout
test_url = 'https://www.baidu.com/'
timeout = 60



def is_valid(proxy):
    try:
        proxies = {
            'https': 'http://' + proxy
        }
        requests.get(test_url, timeout=timeout, proxies=proxies)
        return True
    except (ProxyError, ConnectTimeout, SSLError, ReadTimeout, ConnectionError):
        return False

is_valid('localhost:3129')