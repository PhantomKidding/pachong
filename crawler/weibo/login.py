#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] login.py


from __future__ import print_function

import base64
import binascii
import json
import re

import rsa
from six.moves.urllib.parse import quote


class WeiboLogin(object):

    def __init__(self, session):
        print('正在登录微博...', end='')
        self.session = session

    def get_server_data(self):
        server_url = 'http://login.sina.com.cn/sso/prelogin.php?' \
                     'entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' \
                     'rsakt=mod&client=ssologin.js(v1.4.18)&_=1407721000736'
        serverData = self.session.get(server_url, timeout=10).content
        try:
            # 在JSON中提取serverTime, nonce, pubkey, rsakv字段
            p = re.compile('\((.*)\)')
            json_raw = p.search(serverData).group(1)
            json_data = json.loads(json_raw)
            servertime = str(json_data['servertime'])
            nonce = json_data['nonce']
            pubkey = json_data['pubkey']
            rsakv = json_data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print("失败.")
            return None

    def post_encode(self, username, password, servertime, nonce, pubkey, rsakv):
        return {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': self.encode_username(username),
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'sp': self.encode_password(password, servertime, nonce, pubkey),
            'encoding': 'UTF-8',
            'prelt': '115',
            'rsakv': rsakv,
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }

    def is_logged_in(self):
        mainPage = 'http://s.weibo.com/'
        html = self.session.get(mainPage, timeout=10).content
        p = re.compile('\$CONFIG\[\'islogin\'\] = \'([0-9])\'')
        return p.search(html).group(1) == '1'

    def _login(self, username, password):
        if self.is_logged_in():
            print('已登录!')
            return True

        servertime, nonce, pubkey, rsakv = self.get_server_data()
        redirect = self.session.post('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',
                                     params=self.post_encode(username, password, servertime, nonce, pubkey, rsakv))
        try:
            redirect_url = self.get_redirect_login_url(redirect.content)
            if self.is_redirect_login_url(redirect_url):
                self.session.get(redirect_url, timeout=10)
                return True
            else:
                return False
        except:
            return False

    def login(self, username, password):
        print('登陆成功!') if self._login(username, password) else ('登陆失败. T T')
        return self.session

    @staticmethod
    def encode_username(username):
        return base64.encodestring(quote(username)).strip()

    @staticmethod
    def encode_password(password, servertime, nonce, pubkey):
        rsa_pubkey = int(pubkey, 16)
        key = rsa.PublicKey(rsa_pubkey, 65537)  # 创建公钥
        msg = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文加密文件中得到
        pwd = rsa.encrypt(msg, key)  # 加密
        pwd = binascii.b2a_hex(pwd)  # 将加密信息转换为16进制。
        return pwd

    @staticmethod
    def get_redirect_login_url(text):
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        loginUrl = p.search(text).group(1)
        return loginUrl

    @staticmethod
    def is_redirect_login_url(redirectLoginUrl):
        p = re.compile('retcode=[0-9]+')
        m = p.findall(redirectLoginUrl)
        if 'retcode=0' in m:
            return True
        else:
            print(m)
            return False
