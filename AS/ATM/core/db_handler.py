# Author:  Langkye
# Data:    2019/9/30

"""
数据句柄
"""

import os, sys ,json, time
DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(DIR)))

from conf import settings

def db_handler():   # conn_params
    """
    数据库句柄
    :param conn_params: 链接数据库
    :return:
    """
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass    # todo
    ...

def file_db_handle(conn_params):
    """
    parse the db file path  # 解析数据文件路径
    :param conn_params: the db connection params set in settings
    :return:
    """
    return file_execute

def file_execute(sql, **kwargs):
    """

    :param sql:
    :param kwargs:
    :return:
    """
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])  # ...\AS\ATM/db/user
    sql_list = sql.split('where')

    if sql_list[0].startswith('select') and len(sql_list) > 1:
        # Column:列 ; val:列
        column,val = sql_list[1].strip().split('=')
        if column == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            if os.path.isfile(account_file):
                with open(account_file, 'r') as f:
                    account_data = json.load(f)
                    return account_data
            else:
                exit('\033[31;1m用户 [%s] 不存在!\033[0m' % val)
    elif sql_list[0].startswith('update') and len(sql_list) > 1:
        column, val = sql_list[1].strip().split('=')
        if column == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get('account_data')
                with open(account_file, 'w') as f:
                    acc_data = json.dump(account_data, f)
                return True
