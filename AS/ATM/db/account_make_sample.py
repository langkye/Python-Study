# Author:  Langkye
# Data:    2019/9/30

import json

# 用户数据格式
acc_format = {
    'Account':'95580',       # 账号（银行卡号）
    'Password':'1234',       # 密码
    'Credit':20000,          # 信用卡额度
    'Balance':20000,         # 用余额
    'Recode Date':'2019-01-01',      # 注册日期
    'Expire Date':'2023-12-30',      # 过期日期
    'Repayment Date':29,     # 还款日
    'Status':0,              # 状态。 0：normal(正常); 1: locked(锁定); 2: disabled(无效)
}

if __name__ == '__main__':
    data = json.dumps(acc_format)
    with open('user\\%s.json'%(acc_format['Account']),'w') as f:
        f.write(data)