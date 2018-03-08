#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] weibo.py


from __future__ import absolute_import
from __future__ import unicode_literals

import itertools
import re
import time

from future.builtins import range, input
from selenium.common.exceptions import TimeoutException
from six.moves.urllib.parse import quote, urljoin
from tqdm import trange

from crawler.common.utils import json_has, parse_script, get_page_property
from crawler.weibo.login import WeiboLogin
from crawler.weibo.parsers import parse_weibo, parse_profile, parse_total_page, \
    parse_searchusers, parse_weibostore_taobaourl
from fetcher.requests import Requests
from fetcher.selenium import Browser
from pachong import Pachong


class Weibo(Pachong):
    tasks_available = {
        'timeline': Requests,
        'profile': Requests,
        'searchusers': Browser,
        'weibostore': Requests,
    }

    def login(self, username, password, is_retry=False):
        if isinstance(self.fetcher, Requests):
            self.fetcher.session = WeiboLogin(self.fetcher.session).login(username, password)
        elif isinstance(self.fetcher, Browser):
            if is_retry:
                input('Please manually login and enter anything when you finish.')
            try:
                self.fetcher.get('https://weibo.com/login.php',
                                 until=lambda x: x.find_element_by_id('loginname')).send_keys(username)
                self.fetcher.find(xpath='//input[@type="password"]').send_keys(password)
                self.fetcher.find(xpath='//a[@node-type="submitBtn"]').click()
            except TimeoutException:
                return self.login(username, password, True)
            time.sleep(30)
        return self

    def timeline(self, uid, page_from=None, page_until=None):
        if page_from is None:
            page_from = self.input_.find(uid, ['task.{}.page'.format(self.task)]) \
                .get('task', {}).get(self.task, {}).get('page', 1)

        if page_until is None:
            if 'total_page' not in self.input_.find(uid):
                self.timeline_page(uid, 1)
            page_until = self.input_.find(uid)['total_page']

        with trange(page_from, page_until + 1) as bar:
            for page in bar:
                bar.set_description('page {}'.format(page))
                for weibo in self.timeline_page(uid, page):
                    yield weibo
                self.logger.push('DATABASE', 'User {} page {}.'.format(uid, page))
                self.input_.update(uid, {'task.{}.page'.format(self.task): page})

    def timeline_page(self, uid, page, pagebar=None):
        weibos = []
        if pagebar is None:
            for pagebar in range(-1, 2):
                weibos += self.timeline_page(uid, page, pagebar)
            return weibos
        page_property = self.input_.find(uid).get('page_property', None)
        params = {
            'is_search': '0',
            'visible': '0',
            'is_all': '1',
            'is_tag': '0',
            'profile_ftype': '1',
            'page': page,
        }
        if pagebar == -1:
            self.fetcher.get('https://weibo.com/{}'.format(uid), params=params)
            if page_property is None:
                page_property = get_page_property(
                    self.fetcher.find('script', type='text/javascript', text=re.compile('\\$CONFIG')).get_text(strip=True),
                    var_name='$CONFIG'
                )
                self.input_.update(uid, {'page_property': page_property})

            feed = self.fetcher.find('script',
                                     text=lambda x: json_has(parse_script(x, within='FM\\.view\((.*)\)'),
                                                             attrs={'ns': 'pl.content.homeFeed.index',
                                                                    'domid': re.compile('MyProfileFeed')}))
            if not feed:
                raise LookupError('Weibo feed not found.')
            feed_html = parse_script(feed.text, within='FM\\.view\((.*)\)')
            self.fetcher.build(feed_html['html'])
        else:
            params.update({
                'ajwvr': '6',
                'domain': page_property['domain'],
                'pl_name': 'Pl_Official_MyProfileFeed__23',
                'id': page_property['page_id'],
                'script_uri': '/' + page_property['oid'],
                'feed_type': '0',
                'pagebar': pagebar,
                'pre_page': page,
                'domain_op': page_property['domain'],
                '__rnd': int(self.utc_now() * 1000)
            })
            feed_html = self.fetcher.get_json('http://weibo.com/p/aj/v6/mblog/mbloglist', params=params)
            self.fetcher.build(feed_html['data'])

        total_page = parse_total_page(self.fetcher)
        if total_page > self.input_.find(uid).get('total_page', 0):
            self.input_.update(uid, {'total_page': total_page})

        feed_list = self.fetcher.find_all('div', attrs={'class': 'WB_cardwrap', 'action-type': 'feed_list_item'})
        for weibo in feed_list:
            record = parse_weibo(weibo, target_uid=uid)
            if record:
                weibos.append(record)
        return weibos

    def profile(self, uid):
        self.fetcher.get('https://weibo.com/{}'.format(uid))
        chong = parse_profile(self.fetcher)
        chong.update({'_id': uid})
        yield chong

    def searchusers(self, keyword):
        input_ = self.input_.find(keyword)
        keywordq = quote(quote(keyword.encode('utf-8')))
        adv_params = {'auth': ['per_vip', 'ord'],
                      'gender': ['man', 'women'],
                      'age': ['18y', '22y', '29y', '39y', '40y']}
        adv_params_keys = sorted(adv_params.keys())
        for param_values in itertools.product(*(adv_params[key] for key in adv_params_keys)):

            n_pages = input_.get('task', {}).get('_'.join(param_values), {}).get('total_page', 0)
            page = input_.get('task', {}).get('_'.join(param_values), {}).get('page')
            if page and page == n_pages - 1:
                continue
            if not page:
                n_pages = None

            params = dict(itertools.izip(adv_params_keys, param_values))
            self.fetcher.get('http://s.weibo.com/user/&work={}'.format(keywordq), params=params, delimiter='&')
            if not n_pages and not page:
                n_pages = len(self.fetcher.session.find_element_by_class_name('W_pages')
                              .find_element_by_tag_name('ul')
                              .find_elements_by_tag_name('li')) \
                    if self.fetcher.session.find_elements_by_class_name('W_pages') else 1
                self.input_.update(keyword, {'task.{}.total_page'.format('_'.join(param_values)): n_pages})



            with trange(page if page else 1, n_pages + 1 if n_pages else 51, desc=str(params.values())) as bar:
                for page in bar:
                    time.sleep(20)
                    for user in parse_searchusers(self.fetcher):
                        yield user
                    if page == n_pages:
                        break
                    self.input_.update(keyword, {'task.{}.page'.format('_'.join(param_values)): page})
                    try:
                        next_ = self.fetcher.wait_until(lambda x: x.find_element_by_link_text('下一页'))
                        next_.click()
                    except TimeoutException:
                        break

    def weibostore(self, uid):
        page = 0
        goods = []
        while True:
            page += 1
            store_params = {'weiboUid': uid, '__rnd': int(self.utc_now() * 1000)} \
                if page == 1 else {'weiboUid': uid, 'page': page, 'shopId': ''}
            store_url = urljoin('https://shop.sc.weibo.com/aj/h5/shop/', 'index' if page == 1 else 'recvlist')
            store = self.fetcher.get_json(store_url, params=store_params)
            this_goods = parse_weibostore_taobaourl(store)
            goods += this_goods
            if not this_goods:
                break
        yield {'store_urls': list(set(goods))}
