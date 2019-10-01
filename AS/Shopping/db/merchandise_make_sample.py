# Author:  Langkye
# Data:    2019/10/1

import json
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # ...\AS\Shopping
This_DIR = os.path.dirname(os.path.abspath(__file__))        # ...\AS\Shopping\db
# 商品数据格式
pro_format = {
    'Name':'iphone6s',          # 商品名称
    'Price':'5800',             # 商品价格
    'Master':'Langkye',         # 所属商家
    'Status':0,                 # 状态。 0：normal(正常); 1: locked(锁定); 2: disabled(无效)
    'Classification':'others',  # 商品分类
    # ...
}

if __name__ == '__main__':
    merchandise_list = [("iphone6s   ", 5800), ("mac book   ", 9000), ("coffee     ", 32), ("python book", 80), ("bicycle    ", 1500)]
    for i in range(len(merchandise_list)):      # 循环创建商品
        pro_format['Name'] = merchandise_list[i][0]
        pro_format['Price'] = merchandise_list[i][1]
        data = json.dumps(pro_format)       # 序列化为json格式的数据

        DIR = '%s\\merchandises\\%s\\' % (This_DIR, pro_format['Classification'])
        if not os.path.exists(DIR):     # 判断 当前类型 商品 文件夹 是否存在, 不存在则 创建
            os.makedirs(DIR)
        with open('%s\\%s.json'%(DIR, pro_format['Name'].strip()),'w') as f:    # 保存或更新数据
            f.write(data)