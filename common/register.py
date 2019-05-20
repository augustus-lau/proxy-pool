# -*- coding: utf-8 -*-
import mylogger
import action as ac
import time
import threading
import store as st
logger = mylogger.get_logger(__name__)

'''
    注册机，只用于注册Action, 以便于利用统一管理事件
'''


class Register(object):

    def __init__(self, store=None):
        # 保存所有的action
        self.__actions_list = []
        self.__locker = threading.Lock()
        # 注册机是否已经启动
        self.__started = True
        if isinstance(store, st.Store):
            self.__store = store
        else:
            logger.error(type(store) + ' must be implement of common/store.Store')
            raise Exception

    # 用于注册action
    def register(self, action):

        self.__locker.acquire()
        logger.info('register action [%s]', action.__class__)
        if not action:
            logger.error('action cannot be None. ')
            raise EOFError

        if not isinstance(action, ac.Action):
            logger.error('action should be implement of common/action.Action. ')
            raise EOFError

        if action in self.__actions_list:
            logger.info('action already existed in register, ignore it. ')

        self.__actions_list.append(action)
        self.__locker.release()

    # 返回注册的action数量
    def count(self):
        return len(self.__actions_list)

    # 目前采用循环遍历来调度注册进来的action
    def dispatch_action(self):

        while self.__started:
            logger.info('the size fo proxy in cache is ' + str(self.__store.count()))
            # 刷新缓存的临街条件
            if self.__store.check_refresh():
                for action in self.__actions_list:
                    for item in action.trigger():
                        self.__store.save(item)
                        logger.info('crawled proxy information :' + item)
            time.sleep(60 * 15)

    def start(self):
        self.__started = True

    def stop(self):
        self.__started = False
