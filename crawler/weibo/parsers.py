#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/13/18
# @File  : [pachong] parsers.py

from __future__ import unicode_literals

import json
import re

from six.moves.urllib.parse import parse_qsl

from crawler.common.base62 import mid2str
from crawler.common.utils import keep_int, get_url, get_page_property


def parse_weibo(weibo, target_uid=None, forward_mid=None):
    # media_id
    # timestamp, sent_from
    # forwards, comments, likes
    # media[type[live, video, image], urls, playcount]
    # location
    # content(text, urls)

    if weibo.find('div', class_='WB_empty'):
        return None

    chong = {}

    uid = weibo.find('a', usercard=re.compile('id=')).attrs['usercard']
    chong['uid'] = dict(parse_qsl(uid))['id']

    if target_uid and chong['uid'] != target_uid:
        return None

    mid = weibo.attrs['mid'] if forward_mid is None else forward_mid
    chong['_id'] = mid
    chong['mid62'] = mid2str(mid)

    created_time = weibo.find('a', attrs={'node-type': 'feed_list_item_date'})
    chong['timestamp'] = created_time.attrs['date']

    sent_from = created_time.find_next_sibling('a')
    if sent_from:
        chong['sent_from'] = sent_from.get_text(strip=True)

    handle = weibo.find('div', class_='WB_feed_handle' if forward_mid is None else 'WB_handle')
    forwards_icon = handle.find('em', class_=re.compile('forward'))
    if forwards_icon:
        forwards = keep_int(forwards_icon.next_sibling.get_text(strip=True))
        if forwards:
            chong['forwards'] = forwards
    comments_icon = handle.find('em', class_=re.compile('repeat'))
    if comments_icon:
        comments = keep_int(comments_icon.next_sibling.get_text(strip=True))
        if comments:
            chong['comments'] = comments
    likes_icon = handle.find('em', class_=re.compile('praised'))
    if likes_icon:
        likes = keep_int(likes_icon.next_sibling.get_text(strip=True))
        if likes:
            chong['likes'] = likes

    media_wrap = weibo.find('div', class_=re.compile('media_wrap'))
    if media_wrap:
        picts = media_wrap.find_all('li', class_='WB_pic')
        video = media_wrap.find('li', class_='WB_video')
        chong['media'] = {}
        if picts:
            chong['media']['type'] = 'image'
            chong['media']['urls'] = [get_url(item.img.attrs.get('src', '')) for item in picts]
        elif video:
            video_action = dict(parse_qsl(video.attrs['action-data']))
            chong['media']['type'] = 'video' if 'type' in video_action else 'live'
            chong['media']['urls'] = [get_url(video_action.get('short_url', video_action.get('url')), with_query=False)]
            media_play = video_action.get('play_count', '')
            if media_play:
                chong['media']['play_count'] = media_play
        else:
            other = media_wrap.find('div', class_='WB_feed_spec')
            if other:
                chong['media']['type'] = 'other'

    location_icon = weibo.find('i', class_=re.compile('place'))
    if location_icon:
        location_soup = location_icon.parent
        location_soup.i.extract()
        chong['location'] = location_soup.text
        location_soup.extract()

    content = weibo.find('div', class_='WB_text')
    for icon in content.find_all('i'):
        icon.extract()
    chong['text'] = content.get_text(separator=' ', strip=True).strip('\u200b \t')
    urls = [(item.get_text(strip=True), get_url(item.attrs.get('href', '')))
            for item in content.find_all('a')]
    if urls:
        chong['urls'] = urls

    reweibo = weibo.find('div', {'node-type': re.compile('forwardContent')})
    if reweibo:
        chong['reweibo'] = parse_weibo(reweibo, forward_mid=weibo.attrs['omid'])
    return chong


def parse_profile(fetcher):
    chong = {}

    page_property = get_page_property(
        fetcher.find('script', type='text/javascript', text=re.compile('\\$CONFIG')).get_text(strip=True),
        var_name='$CONFIG')
    chong['page_property'] = page_property

    title_scpt = fetcher.find('script', text=re.compile('"domid": *"Pl_Official_Headerv6__[0-9]"'))
    title_wrap = re.compile('FM\\.view\((.*)\)').search(title_scpt.text).group(1)
    title = fetcher.build(json.loads(title_wrap)['html'], overwrite=False)
    winfo = title.find('div', class_='pf_intro')
    if winfo:
        chong['winfo'] = winfo.get_text(strip=True)
    avatar = title.find('p', class_='photo_wrap')
    if avatar:
        chong['avatar'] = avatar.find('img').get('src')
    if title.find('i', class_=re.compile('icon_pf_female')):
        chong['gender'] = 'f'
    elif title.find('i', class_=re.compile('icon_pf_male')):
        chong['gender'] = 'm'

    profile_scpt = fetcher.find('script', text=re.compile('"domid": *"Pl_Core_UserInfo__[0-9]"'))
    profile_wrap = re.compile('FM\\.view\((.*)\)').search(profile_scpt.text).group(1)
    profile = fetcher.build(json.loads(profile_wrap)['html'], overwrite=False)
    chong['bigV'] = 1 if profile.find('a', class_='icon_verify_v') else 0
    level = profile.find('a', class_='W_icon_level')
    chong['level'] = int(re.compile('Lv\.([0-9]+)').search(level.get_text(strip=True)).group(1))
    location = profile.find('em', class_='ficon_cd_place')
    if location:
        chong['location'] = location.find_next('span').get_text(strip=True)
    edu = profile.find('em', class_='ficon_edu')
    if edu:
        chong['edu'] = re.sub(u'毕业于', u'', edu.find_next('span').get_text(strip=True))
    birthday = profile.find('em', class_='ficon_constellation')
    if birthday:
        chong['birthday'] = birthday.find_next('span').get_text(strip=True)
    pinfo = profile.find('em', class_='ficon_pinfo')
    if pinfo:
        chong['pinfo'] = re.sub(u'简介：[ \t]*', u'', pinfo.find_next('span').get_text(strip=True))
    baidu = profile.find('i', class_='pinfo_icon_baidu')
    if baidu:
        chong['baidu'] = baidu.find_next('a').get('href')
    tags = profile.find('em', class_='ficon_cd_coupon')
    if tags:
        chong['tags'] = [tag.get_text(strip=True) for tag in tags.find_next('span').find_all('a')]
    links = profile.find_all('em', class_='ficon_link')
    if links:
        for link in links:
            if link.find_next('span', class_='item_text').get_text(strip=True).startswith('博客地址'):
                chong['blog'] = link.find_next('a').get('href')
                break

    social_scpt = fetcher.find('script', text=re.compile('"domid": *"Pl_Core_T8CustomTriColumn__[0-9]+"'))
    social_wrap = re.compile('FM\\.view\((.*)\)').search(social_scpt.text).group(1)
    social = fetcher.build(json.loads(social_wrap)['html'], overwrite=False)
    n_following = social.find('a', href=re.compile('mod=headfollow'))
    chong['n_followings'] = int(n_following.strong.text) if n_following else 0
    n_followers = social.find('a', href=re.compile('mod=headfans'))
    chong['n_followers'] = int(n_followers.strong.text) if n_followers else 0
    n_weibos = social.find('a', href=re.compile('mod=data'))
    chong['n_weibos'] = int(n_weibos.strong.text) if n_weibos else 0

    fansgroup_scpt = fetcher.find('script', text=re.compile('"domid": *"Pl_Core_FansGroups__[0-9]+"'))
    if fansgroup_scpt:
        fansgroup_wrap = re.compile('FM\\.view\((.*)\)').search(fansgroup_scpt.text).group(1)
        fansgroup = fetcher.build(json.loads(fansgroup_wrap)['html'], overwrite=False)
        if fansgroup.find('div', class_='obj_name'):
            chong['fansgroup'] = {}
            fetcher.get('https://weibo.com/p/{}/fansgroup?from=fansgroup'.format(page_property['page_id']))
            fansgroup_scpt = fetcher.find('script', text=re.compile('"domid": *"Pl_Official_FansGroupList__[0-9]+"'))
            fansgroup_wrap = re.compile('FM\\.view\((.*)\)').search(fansgroup_scpt.text).group(1)
            fansgroup = fetcher.build(json.loads(fansgroup_wrap)['html'], overwrite=False)
            chong['fansgroup']['count'] = keep_int(fansgroup.find('span', class_='tab_item').get_text(strip=True))
            chong['fansgroup']['members'] = sum(keep_int(li.find('div', text=re.compile('群成员')).get_text(strip=True))
                                                for li in fansgroup.find_all('li', class_='member_li'))

    return chong


def parse_total_page(fetcher):
    pages = fetcher.find('div', class_='W_pages')
    if pages:
        total_page = len(pages.find_all('li'))
        return total_page
    return 1


def parse_searchusers(fetcher):
    users = fetcher.find_all('div', class_='list_person clearfix')
    return [{'_id': user.find_element_by_class_name('W_fb').get_attribute('uid')} for user in users]


def parse_weibostore_taobaourl(data):
    n_goods = len(data['data']['goodsList'])
    if not n_goods:
        return []
    return [good['item_url'] for good in data['data']['goodsList'] if 'taobao' in good['item_url']]
