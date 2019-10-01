# Author:  Langkye
# Data:    2019/9/30

"""
认证
authentic
"""

import os, sys, json, time
DIR = os.path.abspath(__file__)     # 当前脚本路径
sys.path.append(os.path.dirname(os.path.dirname(DIR)))  # 添加 当前项目根目录到python索引列表

from ATM.conf import settings
from ATM.core import db_handler
from ATM.core import logger

def login_required(func):   # 功能拓展
    """
    严重用户是否登录
    :param func: 拓展的函数
    :return:
    """
    def wrapper(*args, **kwargs):
        if args[0].get('is_authenticated'):
            return func(*args, **kwargs)
        else:
            exit('用户未登录')
    return wrapper

def acc_login(user_data, log_obj):
    """
    account login func  # 用户登录函数
    :param user_data:user info data , only saves in memory
    :param log_obj: The log object      # 日志对象
    :return:
    """

    retry_count = 3     # 用户尝试次数
    while user_data['is_authenticated'] is not True and retry_count > 0:
        account = input('\033[32;1m账号:\033[0m').strip()
        password = input('\033[32;1m密码:\033[0m').strip()
        auth = acc_auth(account, password)  # 用户认证
        if auth:
            user_data['is_authenticated'] = True
            user_data['account'] = account
            return auth
        print('\033[32;1m尊敬的 [%s] 用户, 您已输错 [%s] 次!\033[0m\t\033[31;1m您还剩 [%s] 次机会！\033[0m' % (account, 4 - retry_count, retry_count - 1))
        log_obj.warn('账号 [%s] 输错 1 次！' % account)       # 每输错一次 就记录日志
        retry_count -= 1
    else:   # 超过次数，记录日志，退出程序
        log_obj.error('账户 [%s] 尝试次数超限!' % account)      # 只有输错 3 次才能记录日志
        exit()
def acc_auth_ordinary(account, password):
    """
    普通认证接口，局限于文件处理  #  下面的 acc_auth() 已进行优化，可拓展 链接数据库
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , return the account object, otherwise ,return None
           : 如果通过认证，返回从文件加载的用户数据；否则返回空
    """
    db_path = db_handler.db_handler(settings.DATABASE)      # 用户账户路径
    account_file = '%s%s.json' % (db_path, account)     # 用户文件
    if os.path.isfile(account_file):    # 如果本地有该用户数据文件（已经注册的用户）
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                # 信用卡过期时间
                Expire_Time = time.mktime(time.strptime(account_data['Expire Date'], '%Y-%m-%d'))
                if time.time() > Expire_Time:    # 信用卡失效
                    print('\033[31;1m账号 [%s] 已经失效, 请与联系银行办理新的信用卡!\033[0m' % account)
                else:   # 通过认证则返回存储在本地的用户账户数据
                    return account_data
            else:
                print('\033[31;1m账号或密码错误!\033[0m')
    else:
        print('\033[31;1m账户 [%s] 不存在!\033[0m' % account)


def acc_auth(account, password):
    """
    优化认证接口，可拓展数据库
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , return the account object, otherwise ,return None
           : 如果通过认证，返回从文件加载的用户数据；否则返回空
    """
    db_api = db_handler.db_handler()
    data = db_api('select * from account where account=%s' % account)
    if data['Password'] == password:
        Expire_Time = time.mktime(time.strptime(data['Expire Date'], '%Y-%m-%d'))
        if time.time() > Expire_Time:
            print('\033[31;1m账号 [%s] 已经失效, 请与联系银行办理新的信用卡!\033[0m' % account)
        else:
            return data
    else:
        print('\033[31;1m账号或密码错误!\033[0m')