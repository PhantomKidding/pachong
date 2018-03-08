#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/27/18
# @File  : [pachong] taobao.py


from __future__ import unicode_literals

import random
import time

from tqdm import tqdm
from future.builtins import input
from pushbullet import PushBullet

from crawler.taobao.parsers import parse_shop, parse_itemlist, \
    parse_shopid_from_itempage, parse_itempage, parse_comments
from fetcher.requests import Requests
from fetcher.selenium import Browser
from pachong import Pachong
import re
import json


class Taobao(Pachong):

    tasks_available = {
        'shop': (Requests, Browser),
        'itemlist': Browser,
        'shopid2': Requests,
        'itempage': Browser,
        'comments': Requests,
    }

    def generate_ksTS(self, digit=3):
        return ('{:13d}_{:' + str(digit) + 'd}').format(int(self.utc_now() * 1000), int(random.random() * 1000))


    def login(self, username=None, password=None):
        if not username and not password:
            self.fetcher.get('https://login.taobao.com/')
            input('press any after manually logged in.')
            return self
        self.fetcher.get('https://world.taobao.com/markets/all/login')
        self.fetcher.session.switch_to_frame('login-iframe')
        self.fetcher.find('input', name='TPL_username').send_keys(username)
        self.fetcher.find('input', name='TPL_password').send_keys(password)
        self.fetcher.find('button', id='submit').submit()
        while True:
            if 'login' not in self.fetcher.session.current_url:
                break
            self.logger.push('LOGIN', 'Please manually finish verification.')
            time.sleep(30)
            return self

    def captcha_handler(self):
        self.fetcher.session.switch_to_default_content()
        iframe = self.fetcher.find('iframe', id='sufei-dialog-content')
        if iframe:
            self.fetcher.session.switch_to_frame(iframe)
            if self.fetcher.find('div', id='J_LoginBox'):
                self.login()
            elif self.fetcher.find('div', id='J_CodeContainer'):
                input_field = self.fetcher.find('input', type='text', id='J_CodeInput')
                while self.fetcher.find('button', id='J_submit'):
                    input_field.clear()
                    response = self.pb.push_link('淘宝验证', self.fetcher.find('img', id='J_CheckCodeImg1').get_attribute('src'))
                    receive = False
                    while not receive:
                        time.sleep(60)
                        pushes = self.pb.get_pushes()
                        if pushes[1]['iden'] == response['iden']:
                            verfication_code = pushes[0]['body'].strip()
                            receive = True
                    input_field.send_keys(verfication_code)
                    self.fetcher.find('button', id='J_submit').click()
                    time.sleep(15)
            self.fetcher.session.switch_to_default_content()

    def shop(self, _id):
        if self.input_ is self.output:
            self.fetcher.get('https://shop{}.taobao.com/'.format(_id))
        else:
            shopname = self.input_.find(_id).get('taobao_shopname')
            if not shopname:
                raise LookupError('Taobao id not found.')
            self.fetcher.get('https://{}.taobao.com/'.format(shopname))
        chong = parse_shop(self.fetcher)
        chong['weibo_id'] = _id
        yield chong

    def itemlist(self, shopid):
        page = self.input_.find(shopid).get('task', {}).get('itemlist', {}).get('page', 1)
        self.fetcher.get('https://shop{}.taobao.com/search.htm'.format(shopid))

        if page != 1:
            self.captcha_handler()
            pageNo = self.fetcher.find('input', name='pageNo')
            pageNo.clear()
            pageNo.send_keys('{}'.format(int(page)))
            pageNo.submit()
            time.sleep(5)

        _next = True
        while _next:
            self.captcha_handler()
            next_btn = self.fetcher.wait_until(lambda x: x.find_element_by_link_text('下一页'))
            for item in parse_itemlist(self.fetcher):
                yield {'_id': item, 'shopid': shopid}
            self.input_.update(shopid, {'task.itemlist.page': page})
            if next_btn:
                if next_btn.get_attribute('class') == 'disable':
                    _next = False
                else:
                    next_btn.click()
                    page += 1
                    time.sleep(10)
            else:
                raise LookupError('Next page button not found.')

    def itempage(self, itemid):
        self.fetcher.get('https://item.taobao.com/item.htm', params={'id': itemid},
                         until_not=lambda x: x.find_element_by_xpath(
                             '//div[@id="J_DivItemDesc" and contains(text(), "描述加载中")]'))
        chong = parse_itempage(self.fetcher)
        if chong:
            chong['_id'] = itemid
            yield chong

    def comments(self, itemid):
        page = self.input_.find(itemid).get('task', {}).get('comments', {}).get('page', 1)
        bar = tqdm(position=page)
        _next = True
        while _next:
            params = {'auctionNumId': itemid,
                      'userNumId': self.profile.find(self.input_.find(itemid)['shopid'])['seller_id'],
                      'currentPageNum': page,
                      'pageSize': 20,
                      'rateType': '',
                      'orderType': 'orderType:sort_weight',
                      'attribute': '',
                      'sku': '',
                      'hasSku': 'false',
                      'folded': 0,
                      'ua': self.ua,
                      '_ksTS': self.generate_ksTS(4),
                      'callback': 'jsonp_tbcrate_reviews_list'}
            self.fetcher.get('https://rate.taobao.com/feedRateList.htm', params=params)
            _next, chongs = parse_comments(self.fetcher)
            for chong in chongs:
                chong['_id'] = chong.pop('rateId')
                chong['itemid'] = itemid
                yield chong
            self.input_.update(itemid, {'task.comments.page': page})
            page += 1
            bar.update(1)

    def shopid2(self, weibo_uid):
        doc = self.input_.find(weibo_uid)
        if doc.get('task', {}).get('shopid_manual', {}).get('status') != 'done':
            with tqdm(doc.get('store_urls', [])) as items:
                shopids = dict()
                for item_url in items:
                    self.fetcher.get(item_url)
                    shopid = parse_shopid_from_itempage(self.fetcher)
                    if shopid:
                        if shopid in shopids:
                            shopids[shopid] += 1
                        else:
                            shopids[shopid] = 1
                            # yield {'taobao_id': shopid}
                            # break
                time.sleep(random.random())
            if len(shopids) > 1:
                yield {'taobao_shopid': shopids}
            elif len(shopids) == 1:
                yield {'taobao_shopid': shopids.keys[0]}

    def set_pushbullet(self, token):
        self.pb = PushBullet(token)
        return self

    @property
    def ua(self):
        return self._ua

    @ua.setter
    def ua(self, val):
        self._ua = val


