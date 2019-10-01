# Author:  Langkye
# Data:    2019/9/30

"""
主要逻辑
main program handle module , handle all the user interaction stuff
access : 访问
"""

import os, sys, json, re

from ATM.core.auth import login_required

DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(DIR)))

from ATM.core import auth
from ATM.core import logger
from ATM.core import accounts
from ATM.core import transaction
from ATM.conf import settings
from ATM import db
from ATM import log

# transaction logger
# 交易日志记录对象
trans_logger = logger.logger('transaction')

# 访问日志对象
access_logger = logger.logger('access')

# temp account data ,only saves the data in memory
# 临时帐户数据，只保存在内存中的数据(安全性。防止程序突然崩掉，使得用户处于上一次登录登录状态)
user_data = {
    'account':None,             # 初始为空
    'is_authenticated':False,   # 状态为 “未登录”
    'account_data':None,        # 初始为空
}

def account_info(acc_data):
    """
    1.用户信息  # 这里必须要从本地数据库（文件）中获取用户实时数据
    :param acc_data: 用户数据
    :return:
    """
    # 加载最新的 账号信息
    account_data = accounts.load_current_balance(acc_data['account'])
    acc_info = u"""
────────────── 您的账单详情 ──────────────
│            当前账号:  {Account}\t\t\t│
|            信用额度:  {Credit}\t\t\t│
|            当前余额:  {Balance}\t\t\t│
|            注册时间:  {Enroll_Data}\t\t│
|            过期时间:  {Expire_Data}\t\t│
|            还款时间:  {Pay_Data}\t\t\t\t│
|            当前状态:  {Status}\t\t\t\t│
└────────────────── End ─────────────────
        """.format(Account=account_data['Account'], Credit=account_data['Credit'], \
                   Balance=account_data['Balance'], Enroll_Data=account_data['Recode Date'], \
                   Expire_Data=account_data['Expire Date'], Pay_Data=account_data['Repayment Date'], \
                   Status=account_data['Status'])
    print(acc_info,end='')

@login_required
def repay(acc_data):
    """
    print current balance and let user repay the bill
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account'])
    current_balance = u'''────────────── 余额信息 ──────────────
        信用额度:    %s
        当前余额:    %s
        [输入存款金额]
        [‘b’返回上层菜单]
──────────────────End────────────────────''' % (account_data['Credit'], account_data['Balance'])
    print(current_balance)

    back_flag = False
    while not back_flag:
        repay_amount = input('\033[33;1m请输入存款金额!')
        if repay_amount == 'b' or repay_amount == 'B':
            back_flag = True
        elif len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1m您的余额为：%s\033[0m''' % new_balance['Balance'])
        else:
            print('''\033[31;1m[%s] 不是有效的金额, 请输入合理的数值!\033[0m''' % repay_amount)

def withdraw(acc_data):
    """
    # 打印当前余额，让用户进行取款操作
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account'])
    current_balance = '''────────────────余额信息──────────────────
            信用额度:    %s
            当前余额:    %s
            \033[32;1mInput <b> To back\033[0m''' % (account_data['Credit'], account_data['Balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1m请输入取款金额:\033[0m").strip()
        if withdraw_amount == 'b' or withdraw_amount == 'B':
            back_flag = True
        elif len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,  account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1m当前余额为:%s\033[0m''' % (new_balance['Balance']))
        else:
            print('\033[31;1\033[31;1m[%s] 不是有效的金额, 请输入合理的数值!\033[0m' % withdraw_amount)

def transfer(acc_data):
    """
    :param acc_data:
    :return:
    """
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])  # ...\AS\ATM/db/user
    account_data = accounts.load_current_balance(acc_data['account'])
    current_balance = '''────────────────余额信息──────────────────
                信用额度:    %s
                当前余额:    %s
                 \033[32;1mInput <b> To back\033[0m''' % (account_data['Credit'], account_data['Balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:        # ----------------------
        a = input('\033[33;1m请输入【对方】账号:\033[0m').strip()
        if a == 'b' or a == 'B':
            back_flag = True
        elif a.isdigit():
            trans_account = int(a)
            # 账号是否存在
            trans_account_path = '%s/%s.json' % (db_path, trans_account)
            if os.path.isfile(trans_account_path):
                with open(trans_account_path, 'r') as f:
                    trans_data = json.load(f)
                trans_amount = input("\033[33;1m请输入【转出】金额:\033[0m").strip()
                if trans_amount == 'b' or trans_amount == 'B':
                    back_flag = True
                elif len(trans_amount) > 0 and trans_amount.isdigit():
                    new_balance = transaction.make_transaction(trans_logger,  account_data, 'transfer', trans_amount)
                    if new_balance:
                        transaction.make_transaction(trans_logger, trans_data, 'repay', trans_amount)
                        print('''\033[42;1m当前余额为:%s\033[0m''' % (new_balance['Balance']))
                else:
                    print('\033[31;1\033[31;1m[%s] 不是有效的金额, 请输入合理的数值!\033[0m' % trans_amount)
            else:
                print('\033[32;1m您输入的账号不存在!\033[0m')
        else:
            print('\033[32;1m输入错误，请重试!\033[0m')

def pay_check(acc_data):
    """
    :param acc_data: {'account': '95580', 'is_authenticated': True, 'account_data': {'Account': '95580', 'Password': '1234', 'Credit': 20000, 'Balance': 20100.95, 'Recode Date': '2019-01-01', 'Expire Date': '2023-12-30', 'Repayment Date': 29, 'Status': 0}}
    :return:
    """
    trans_log_file = '%s/log/transaction.log' % settings.BASE_DIR   # 交易日志路径
    trans_data_list = []
    if os.path.isfile(trans_log_file):
        with open(trans_log_file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if acc_data['account'] in line:
                    trans_data_list.append(line)
    bill = ''
    print('────────────────────────────────────────────────────── Your Bill ──────────────────────────────────────────────────────')
    if len(trans_data_list) < 10:
        view = len(trans_data_list) + 1
    else:
        view = 11
    for i in range(1,view):
        print('\t\033[34;1m',trans_data_list[-i],'\033[0m')
    print('──────────────────────────────────────────────────────────End──────────────────────────────────────────────────────────')

def logout(acc_data):
    """
    :param acc_data:
    :return:
    """
    exit('退出成功')

def run():
    """
    该方法在程序启动时被调用，处理用户的交互
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    acc_data = auth.acc_login(user_data, access_logger)     # 登录认证
    if user_data['is_authenticated']:   # 登录状态
        user_data['account_data'] = acc_data    # 将用户数据临时存入user_data（内存）
        interactive(user_data)      # 进行查询、转账...等一系列的操作

def interactive(acc_data):
    """
    用户交互
    :param acc_data: account data
    :return:
    """
    menu = u'''
────────────── LangKye Bank ──────────────\033[32;1m
               1.  账户信息                       
|              2.  存   款                |
|              3.  取   款                |
|              4.  转   账                |
|              5.  账   单                |
|              6.  退   出                |\033[0m
└─────────────────End─────────────────────'''

    menu_dict = {
        '1':account_info,
        '2':repay,
        '3':withdraw,
        '4':transfer,
        '5':pay_check,
        '6':logout,
    }

    exit_flag = False   # 退出标志
    while not exit_flag:
        print(menu)
        user_option = input('>>>:').strip()  # 用户输入指令，去掉多余的空字符串
        if user_option in menu_dict:
            menu_dict[user_option](acc_data)
        else:
            print('\033[31;1m选项不存在!\033[31;0m')

if __name__ == '__main__':
    run()