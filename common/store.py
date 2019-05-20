# -*- coding: utf-8 -*-
import mylogger
logger = mylogger.get_logger(__name__)

'''
    用于存储端的接口，供子类实现
'''


class Store(object):

    # 保存数据
    def save(self, item):
        pass

    # 刷新缓存的临界条件
    def check_refresh(self):
        pass

    def count(self):
        pass

    def get_proxy(self):
        pass
