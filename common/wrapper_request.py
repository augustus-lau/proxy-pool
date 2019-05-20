# -*- coding: utf-8 -*-

import requests
import random
import time
import mylogger
logger = mylogger.get_logger(__name__)
__author__ = 'Augustus'

'''
    用于封装Request, 随机设置不同的请求头
'''


class WrapperRequest(object):

    def __init__(self, store=None):
        self.__store = store

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)

    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8'}

    def get(self, url, header=None, retry_time=2, timeout=30,
            retry_interval=2, *args, **kwargs):
        """
        get method
        :param url: target url
        :param header: headers
        :param retry_time: retry time when network error
        :param timeout: network timeout
        :param retry_interval: retry interval(second)
        :param args:
        :param kwargs:
        :return:
        """
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        retry_num = 0
        time.sleep(retry_interval)
        while retry_num < retry_time:
            try:
                logger.info('[' + url + ']')
                # 每期请求前，从redis中获取一个代理信息
                proxies = None
                proxy = self.__store.get_proxy()
                if proxy:
                    proxies = {'http:': proxy}
                resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies, **kwargs)
                if resp.status_code == 200 and resp.content:
                    # 如果可用，再将item保存到库中
                    if proxy:
                        self.__store.save(proxy)
                    return resp.content
                else:
                    logger.error('response code : ' + str(resp.status_code))
                    raise Exception
            except Exception as e:
                logger.error(e)
                retry_num += 1
