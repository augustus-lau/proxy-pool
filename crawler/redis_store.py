# -*- coding: utf-8 -*-
from common import mylogger
from common import store as st
import redis
logger = mylogger.get_logger(__name__)

# redis中存储的代理list的key
PROXY_LIST_KEY = 'proxy:list'


class RedisStore(st.Store):

    def __init__(self, port=6379, host='127.0.0.1', password=None):
        self.r = redis.Redis(host=host, port=port, password=password)

    # proxy保存入redis
    def save(self, item):
        self.r.lpush(PROXY_LIST_KEY, item)

    # 数据量小于30时，触发刷新
    def check_refresh(self):
        return self.r.llen(PROXY_LIST_KEY) < 30

    def count(self):
        return self.r.llen(PROXY_LIST_KEY)

    # 每次取20条数据
    def get_proxy(self):
        return self.r.rpop(PROXY_LIST_KEY)
