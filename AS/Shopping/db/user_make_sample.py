# Author:  Langkye
# Data:    2019/10/1


import json

# 用户数据格式
user_format = {
    'ID':'langkye',          # 账号（银行卡号）
    'Password':'1234',       # 密码
    'Recode Date':'2019-01-01',      # 注册日期
    'Expire Date':'2023-12-30',      # 过期日期
    'Level':2,              # 状态。 0：客户; 1: 商家; 2：管理员
}

if __name__ == '__main__':
    data = json.dumps(user_format)
    with open('user\\%s.json'%(user_format['ID']),'w') as f:
        f.write(data)