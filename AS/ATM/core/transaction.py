# Author:  Langkye
# Data:    2019/9/30

"""
抽离交易的共性：金额的‘加’、‘减’
"""
import os
import sys

DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(DIR)))

from ATM.conf import settings
from ATM.core import accounts

def make_transaction(log_obj, account_data, tran_type, amount, **others):
    """
    # 处理所有用户的交易事务
    deal all the user transactions
    :param log_obj:
    :param account_data: user account data
    :param tran_type: transaction type
    :param amount: transaction amount
    :param others: mainly for logging usage
    :return:
    """

    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = account_data['Balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest
            if new_balance < 0:
                print('''\033[31;1m您当前的信用额度 [%s] 不够完成这笔交易 [-%s], 您当前的余额为 [%s]''' % (account_data['Credit'], (amount + interest), old_balance))
                return
        account_data['Balance'] = new_balance
        accounts.dump_account(account_data)         # 将当前的余额存入数据库（文件）
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                     (account_data['Account'], tran_type, amount, interest))
        return account_data
    else:
        print("\033[31;1m该交易类型 [%s] 不存在!\033[0m" % tran_type)
