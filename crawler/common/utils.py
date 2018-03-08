#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] utils.py

import json
import re

from future.utils import iteritems
from six.moves.urllib.parse import urlsplit, parse_qsl


def parse_url_args(url):
    return dict(parse_qsl(urlsplit(url).query))


def keep_int(text):
    res = re.sub('[^0-9]', '', text)
    return int(res) if res else 0


def keep_float(text):
    res = re.sub('[^0-9.]', '', text)
    return float(res) if res else 0.


def get_url(url, with_query=True):
    if url is None:
        return url
    url = ('https:' if url.startswith('//') else '') + url
    if not with_query:
        url = url.split('?', 1)[0]
    return url


def json_has(data, attrs):
    for key, val in iteritems(attrs):
        if isinstance(val, re._pattern_type):
            if not val.search(data.get(key)):
                return False
        elif isinstance(val, (str, unicode)):
            if data.get(key) != val:
                return False
    return True


def get_page_property(jscript, var_name):
    if var_name.startswith('$'):
        var_name = var_name[1:]
    for line in jscript.splitlines():
        line = re.sub('\\$|var |;$', '',line.strip())
        if re.compile(var_name).search(line):
            try:
                exec(line)
            except:
                pass
    return eval(var_name)


def parse_script(script, within=None):
    if within:
        if isinstance(within, (str, unicode)):
            within = re.compile(within)
        if isinstance(within, re._pattern_type):
            script = within.search(script)
            if script is None:
                return json.loads('{}')
            script = script.group(1)
    return json.loads(script)