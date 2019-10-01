# Author:  Langkye
# Data:    2019/10/1

import os, sys

DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(DIR)))

from ATM.conf import settings

trans_log_file = '%s/log/transaction.log' % settings.BASE_DIR  # 交易日志路径
trans_data_list = []
if os.path.isfile(trans_log_file):
    # while
    with open(trans_log_file, 'r') as f:
        # trans_data = f.readlines()
        # print(trans_data)
        # print('='*20)
        # print(len(trans_data))
        for line in f.readlines():
            line = line.strip()

            print(line)
#
# for line in fo.readlines():  # 依次读取每行
#     line = line.strip()  # 去掉每行头尾空白
#     print
#     "读取的数据为: %s" % (line)

# 关闭文件

print('-' * 20)
print(trans_data_list)