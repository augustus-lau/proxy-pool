# -*- coding: utf-8 -*-

from common import mylogger
from common import action as ac
from bs4 import BeautifulSoup
from common import wrapper_request as req
from common import register
from crawler import redis_store
import re
logger = mylogger.get_logger(__name__)

# 用代理抓取代理信息
proxy_list = None
# 全局请求器
request = None


# https://www.kuaidaili.com/free/
class Kuaidaili(ac.Action):

    def trigger(self):
        # 最大抓取50页数据
        max_page = 50
        urls = ['https://www.kuaidaili.com/free/inha/{page_size}',
                'https://www.kuaidaili.com/free/intr/{page_size}']

        for u in urls:
            for page in range(1, max_page+1, 1):
                url = u.format(page_size=page)
                content = request.get(url)
                soup = BeautifulSoup(content, 'html.parser')
                proxy_table = soup.find('table')
                if proxy_table:
                    proxy_trs = proxy_table.findAll('tr')[1:]
                    for item in proxy_trs:
                        tds = item.findAll('td')
                        yield tds[0].text.strip() + ":" + tds[1].text.strip()


# https://www.xicidaili.com/nn/
class XiciDaili(ac.Action):

    def trigger(self):

        #
        max_page = 20

        """
                西刺代理 http://www.xicidaili.com
                :return:
                """
        url_list = [
            'https://www.xicidaili.com/nn/',  # 高匿
            'https://www.xicidaili.com/nt/',  # 透明
        ]

        for each_url in url_list:

            for i in range(1, max_page + 1):
                page_url = each_url + str(i)
                content = request.get(page_url)
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    soup_list = soup.find(id="ip_list").findAll('tr')[1:]
                    for item in soup_list:
                        tds = item.findAll('td')
                        yield tds[1].text + ":" + tds[2].text


class Ip66(ac.Action):

    # 提取的ip数量,最大提取300条
    count = 300

    def trigger(self):
        """
                代理66 http://www.66ip.cn/
                :param count: 提取数量
                :return:
                """
        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={count}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={count}"
            "&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip",
        ]

        for u in urls:
            url = u.format(count=300)
            content = request.get(url)
            if content:
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", content)
                for ip in ips:
                    yield ip.strip()


class IP89(ac.Action):
    # 提取的ip数量,最大提取500条
    count = 500

    def trigger(self):
        """
            代理89 http://www.89ip.cn/
            :param count: 提取数量
            :return:
        """
        url_89 = 'http://www.89ip.cn/tqdl.html?num={count}&address=&kill_address=&port=&kill_port=&isp='
        url = url_89.format(count=500)
        content = request.get(url)
        if content:
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", content)
            for ip in ips:
                yield ip.strip()


# http://www.iphai.com
class IPHai(ac.Action):

    def trigger(self):

        urls = ['http://www.iphai.com/free/ng',
                'http://www.iphai.com/free/np',
                'http://www.iphai.com/free/wg',
                'http://www.iphai.com/free/wp']

        for url in urls:
            content = request.get(url)
            soup = BeautifulSoup(content, 'html.parser')
            if not soup:
                continue
            proxy_table = soup.find('table')
            if proxy_table:
                proxy_trs = proxy_table.findAll('tr')[1:]
                for item in proxy_trs:
                    tds = item.findAll('td')
                    yield tds[0].text.strip() + ":" + tds[1].text.strip()


# http://www.ip3366.net
class YunDaili(ac.Action):
    def trigger(self):

        max_page = 5
        # 最大抓取5页数据
        urls = ['http://www.ip3366.net/free/?stype=2&page={page_size}',
                'http://www.ip3366.net/free/?stype=1&page={page_size}']

        for u in urls:
            for page in range(1, max_page + 1, 1):
                url = u.format(page_size=page)
                content = request.get(url)
                if not content:
                    continue
                soup = BeautifulSoup(content, 'html.parser')
                proxy_table = soup.find('table')
                if proxy_table:
                    proxy_trs = proxy_table.findAll('tr')[1:]
                    for item in proxy_trs:
                        tds = item.findAll('td')
                        yield tds[0].text.strip() + ":" + tds[1].text.strip()


if '__main__' == __name__:
    # 注册存储类
    rs = redis_store.RedisStore()
    # 全局请求器
    request = req.WrapperRequest(store=rs)

    # 注册代理的Action
    reg = register.Register(store=rs)

    # 注册代理Action
    reg.register(Kuaidaili())
    reg.register(XiciDaili())
    reg.register(Ip66())
    reg.register(IP89())
    reg.register(YunDaili())
    reg.dispatch_action()
