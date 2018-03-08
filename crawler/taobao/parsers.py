#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/28/18
# @File  : [pachong] parsers.py


from __future__ import unicode_literals

import json
import re
from fetcher.requests import Requests
from crawler.common.utils import keep_int, keep_float


def parse_shop(fetcher):
    error = fetcher.find('div', class_='error-notice-hd')
    if error and error.text.strip() == '没有找到相应的店铺信息':
        return None

    chong = {}

    property = fetcher.find('script', text=re.compile('shop_config'))
    if not property:
        raise LookupError('Page property is not found.')
    shop_config = re.compile('window\.shop_config = (\{[^;]+\});') \
        .search(property.text if isinstance(fetcher, Requests) else property.get_attribute('text'))
    if not shop_config:
        raise LookupError('Shop configuration is not found.')
    config = json.loads(shop_config.group(1))
    chong['_id'] = config['shopId']
    chong['seller_id'] = config['userId']
    chong['category_id'] = config['shopCategoryId']

    # chong['widgetid'] = fetcher.find('div', class_='J_TLayout').attrs['data-widgetid']
    return chong


def parse_itemlist(fetcher):
    return {item.get_attribute('data-id')
            for item in fetcher.find('div', id='J_ShopSearchResult')
                .find_elements_by_xpath('//dl[@data-id and contains(@class, "item ")]')}


def parse_itempage(fetcher):

    if fetcher.find('div', class_='error-notice-hd', text=re.compile('很抱歉，您查看的宝贝不存在，可能已下架或者被转移')):
        return None

    chong = dict()

    chong['title'] = fetcher.find('h3', class_='tb-main-title').text
    if fetcher.find('div', class_=re.compile('tb-off-sale')):
        chong['stock'] = 0
    else:
        chong['stock'] = keep_int(fetcher.find('span', id='J_SpanStock').text)

    chong['price'] = fetcher.find('strong', id='J_StrPrice').find_element_by_class_name('tb-rmb-num').text
    promo = fetcher.find('em', id='J_PromoPriceNum')
    if promo:
        chong['promo'] = promo.text

    chong['comments'] = keep_int(fetcher.find('strong', id='J_RateCounter').text)
    chong['sales'] = keep_int(fetcher.find('strong', id='J_SellCounter').text)
    chong['bookmarks'] = keep_int(fetcher.find('em', class_='J_FavCount').text)

    cover = fetcher.find('ul', id='J_UlThumb')
    if cover:
        chong['cover'] = dict()
        video = cover.find_elements_by_id('J_VideoThumb')
        if video:
            fetcher.move_to(video[0])
            fetcher.find('button', class_=re.compile('vjs-center-start')).click()
            chong['cover']['video'] = fetcher.find('video', class_='lib-video').get_attribute('src')
        chong['cover']['images'] = [re.sub('_[0-9]+x[0-9]+\\.jpg$', '',
                                           img.find_element_by_tag_name('img').get_attribute('data-src'))
                                    for img in cover.find_elements_by_xpath('//li[@data-index]')
                                    if img.find_element_by_tag_name('img').get_attribute('data-src')]

    charity = fetcher.find('div', id='J_PublicWelfare')
    if charity and charity.get_attribute('style') != 'display: none;':
        chong['charity'] = charity.find_element_by_class_name('infoBox').text

    chong['attributes'] = [re.split(u' *[:\uff1a] *', li.text)[-2:] for li in
                           fetcher.find('div', id='attributes').find_elements_by_tag_name('li')
                           if li.text.strip()]

    description = fetcher.find('div', id='J_DivItemDesc')
    if description:
        chong['description'] = {}
        if description.text:
            chong['description']['text'] = description.text.strip()
        chong['description']['images'] = [img.get_attribute('src')
                                          for img in description.find_elements_by_tag_name('img')]


    return chong


def parse_comments(fetcher):
    p = fetcher.find('p')
    if not p:
        raise LookupError(''.format(fetcher.source_code()))
    comments = json.loads(p.text.strip()[27: -1])
    has_next = comments['maxPage'] - comments['currentPageNum']
    chongs = [comment for comment in comments['comments']]
    return has_next, chongs



def parse_shopid_from_itempage(fetcher):
    error = fetcher.find('div', class_='error-notice-hd')
    if error and error.text.strip() =='很抱歉，您查看的宝贝不存在，可能已下架或者被转移。':
        return None

    property = fetcher.find('script', text=re.compile('var g_config'))
    if property:
        shopid_line = [line.strip('\t },;') for line in re.split('\n', property.text)
                       if line.strip('\t },;').startswith('shopId')]
        if shopid_line:
            return re.compile(': +\'([0-9]+)\'').search(shopid_line[0]).group(1)
    return None
