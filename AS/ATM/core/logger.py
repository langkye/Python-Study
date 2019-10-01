# Author:  Langkye
# Data:    2019/9/30

"""
整个程序的日志工作

    'application' code:
        日志级别：
        logger.debug('debug message')   # 调试
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
"""

import logging, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ATM.conf import settings

def logger(log_type):
    """

    :param log_type: 登录、流水账...
    :return:
    """

    # 创建日志对象  ； 设置日志级别
    loggers = logging.getLogger(log_type)
    loggers.setLevel(settings.FH_LOG_LEVEL)

    # 创建控制台处理程序并设置要调试的级别(控制台输出)
    ch = logging.StreamHandler()
    ch.setLevel(settings.CH_LOG_LEVEL)

    # 创建文件处理程序并将级别设置为警告
    log_file = '%s/log/%s' % (settings.BASE_DIR, settings.LOG_TYPE[log_type])
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(settings.FH_LOG_LEVEL)

    # 创建日志记录格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 给日志输出流和日志记录流添加格式
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 将控制台输出 和 记录 添加到日志对象中
    loggers.addHandler(ch)
    loggers.addHandler(fh)

    return loggers