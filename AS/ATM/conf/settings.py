# Author:  Langkye
# Data:    2019/9/30

import os
import logging

# AT 相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # ...\AS\ATM
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
    'repay':{               # 存款
        'action':'plus',    # 动作为 “加”
        'interest':0,       # 利息为 “0”
    },
    'withdraw':{            # 取款
        'action':'minus',   # 动作为 “减”
        'interest':0.05,    # 利息为 “0.05”
    },
    'transfer':{            # 转账
        'action':'minus',   # 动作为 “减”
        'interest':0.04,    # 利息
    },
    'consume':{             # 消费
        'action':'minus',   # 动作为 “减”
        'interest':0,       # 利息
    },
}

# 访问