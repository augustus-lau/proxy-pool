# -*- coding: utf-8 -*-

'''
    Action代表一个事件
'''


class Action(object):

    # 用于子类继承, 这是一个Action的触发器，实现用于触发的事件
    def trigger(self):
        pass
