# Author:  Langkye
# Data:    2019/10/1

import os
import logging

# AT 相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # ...\AS\Shopping
DATABASE = {
    'engine':'file_storage',    # support mysql, postGreSql in the future
    'name':'user',
    'path':'%s/db' % BASE_DIR
}


'''
'application' code:
        日志级别：
        logger.debug('debug message')   # 调试
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')

'''
FH_LOG_LEVEL = logging.INFO    # 文件日志级别
CH_LOG_LEVEL = logging.ERROR   # 控制台
LOG_TYPE = {                # 日志类型
    'transaction':'transaction.log',    # 账号交易日志
    'access':'access.log',             # 用户访问受限日志，即输错3次密码，将被记入日志
}

# 交易
TRANSACTION_TYPE = {
    'add':{                 # 加入购物车
        'action':'plus',    # 动作为 “加”
    },
    'sub':{                 # 移出购物车
        'action':'minus',   # 动作为 “减”
    },
    'consume':{             # 消费
        'action':'minus',   # 动作为 “减”
        'interest':0,       # 利息
    },

}

# 访问

# 商品价格