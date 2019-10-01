# Author:  Langkye
# Data:    2019/9/30

"""
用户账户
"""

import os, sys, json
# AT 相对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from ATM.core import db_handler
from ATM.conf import settings

def load_current_balance(account_id):
    """
    # 返回当前账户信息
    return account balance and other basic info
    :param account_id:
    :return:
    """
    db_api = db_handler.db_handler()
    data = db_api('select * from account where account=%s' % account_id)
    return data

def dump_account(account_data):
    """
    # 更新事务或帐户数据后，将其转储回文件db
    after updated transaction or account data , dump it back to file db
    :param account_data:
    :return:
    """
    db_api = db_handler.db_handler()
    data = db_api("update user where account=%s" % account_data['Account'], account_data=account_data)

    return True