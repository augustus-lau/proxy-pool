# -*- coding: utf-8 -*-
import sys
import logging

reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 获取Logger
def get_logger(class_name=None):
    return logging.getLogger(class_name)

