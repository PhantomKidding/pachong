#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cheng Chen
# @Email : cchen224@uic.edu
# @Time  : 2/28/18
# @File  : [pachong] proxy.py



from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

PROXY = "localhost:3128"
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver.close()
driver = webdriver.Chrome('/Users/cchen/Programs/webdriver/chromedriver', chrome_options=chrome_options)
driver.get('https://item.taobao.com/item.htm?ut_sk=1.VhKLoEf4u7MDAN5xQlvmmE9v_21380790_1497248494954.Copy.1&id=553095985111&sourceType=item&price=188&suid=77ABCEE5-A28F-4AB1-9344-BD237B7312CE&cv=gb82ZDMEBRW&sm=24412f')

# driver.get('https://weibo.com')



import urllib2
import time
import random
import re
import gzip
import StringIO
def set_proxy():
    """
    设置代理
    """
    # 获取xicidaili的高匿代理
    proxy_info_list = []  # 抓取到的ip列表
    for page in range(1, 11):  # 暂时只抓第一页
        request = urllib2.Request('http://www.xicidaili.com/nn/%d' % page)
        request.add_header('Accept-Encoding', 'gzip, deflate')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36')
        response = urllib2.urlopen(request, timeout=5)

        headers = response.info()
        content_type = headers.get('Content-Type')
        if content_type:
            charset = re.findall(r"charset=([\w-]+);?", content_type)[0]
        else:
            charset = 'utf-8'
        if headers.get('Content-Encoding') == 'gzip':
            gz = gzip.GzipFile(fileobj=StringIO.StringIO(response.read()))
            content = gz.read().decode(charset)
            gz.close()
        else:
            content = response.read().decode(charset)
        response.close()
        print u'获取第 %d 页' % page
        ip_page = re.findall(r'<td>(\d.*?)</td>', content)
        proxy_info_list.extend(ip_page)
        time.sleep(random.choice(range(1, 3)))

    # 打印抓取的内容
    print u'代理IP地址\t端口\t存活时间\t验证时间'
    for i in range(0, len(proxy_info_list), 4):
        print u'%s\t%s\t%s\t%s' % (proxy_info_list[i], proxy_info_list[i + 1], proxy_info_list[i + 2], proxy_info_list[i + 3])

    all_proxy_list = []  # 待验证的代理列表
    # proxy_list = []  # 可用的代理列表
    for i in range(0, len(proxy_info_list), 4):
        proxy_host = proxy_info_list[i] + ':' + proxy_info_list[i + 1]
        all_proxy_list.append(proxy_host)

    # 开始验证

    # 单线程方式
    for i in range(len(all_proxy_list)):
        proxy_host = ping(all_proxy_list[i])
        if proxy_host:
            break
    else:
        # TODO 进入下一页
        print u'没有可用的代理'
        return None

    # 多线程方式
    # threads = []
    # # for i in range(len(all_proxy_list)):
    # for i in range(5):
    #     thread = threading.Thread(target=test, args=[all_proxy_list[i]])
    #     threads.append(thread)
    #     time.sleep(random.uniform(0, 1))
    #     thread.start()
    #
    # # 等待所有线程结束
    # for t in threading.enumerate():
    #     if t is threading.currentThread():
    #         continue
    #     t.join()
    #
    # if not proxy_list:
    #     print u'没有可用的代理'
    #     # TODO 进入下一页
    #     sys.exit(0)
    print u'使用代理： %s' % proxy_host
    return proxy_host
    # urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler({'http': proxy_host})))


import subprocess
from multiprocessing import Pool, cpu_count

hosts = ('117.24.20.163:42905', 'google.com', '127.0.0.2', '10.1.1.1')

def ping(host):
    ret = subprocess.call(['ping', '-c', '5', '-W', '3', host], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    return ret == 0
ping(hosts[0])