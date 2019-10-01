# Author:  Langkye
# Data:    2019/9/6

def main():

    print("\n\t\t\t欢迎光临langkye商城！！！\n")

    go_shopping = True		# 程序运行标志
    buy_git_num = []		# 存储用户选择商品编号

    merchandise_info = [("iphone6s   ", 5800), ("mac book   ", 9000), ("coffee     ", 32), ("python book", 80), ("bicycle    ", 1500)]		# 商品信息

    """	# 1、利用枚举遍历打印商品列表
    for i, v in enumerate(merchandise_info, 1):
         print("\t\t\t%d、%s\t\t￥%d"%(i, v[0], v[1]))
    """
    # 2、利用for , 以及python内置的 .index() 方法取其下标 , 打印商品列表
    str1 = "<商品列表>"
    print(str1.center(42, "-"))
    for name_into in merchandise_info:
        print("\t\t\t%d、%s\t￥%d"%(merchandise_info.index(name_into), name_into[0], name_into[1]))

    print("-"*46)
    salary_input_flag = True		# 用户工资输入标志
    while salary_input_flag:	# 当salary_input_flag的值为真, 即salary_input_flag = True时, 进行循环
        salary = input("请输入您的工资：\t>>>")	# 接受用户的输入

        if salary.isdigit():	# 通过 .isdigit() 方法 判断输入的字符是否为数字
           salary = int(salary)		# 是“数字”, 则将其转为整型
           salary_input_flag = False	# 将工资输入标志设为假, 即salary_input_flag = False , 结束该层循环

        else:	# 输入的工资不是“数字”, 重新输入
            salary_input_flag = True		# 将工资输入标志设为真, 即salary_input_flag = True , 继续该层循环
            print("\n工资输入错误！！！\n")

    while go_shopping:		# 当go_shopping 的值为 True 时 , 开始该循环
        buy_input_flag = True	# 用户购买商品标志

        while buy_input_flag:	# 当 buy_input_flag 的值为 True ,开始购买循环
            Quit = False	# 初始化退出标志 为 False
            choice = input("请选择您的预购商品或退出[0/1/2/3/4][q]：\t>>>")

            if choice.isdigit():	# 判断用户输入的商品号是否为“数字”
                choice = int(choice)	# 是“数字”, 则将其转为整型

                if choice >= 0 and choice <= len(merchandise_info):		# 判断用户输入的商品号是否存在
                    buy_git_num.append(choice)	# 存在, 则将其添加到加入购物车的列表中
                    buy_input_flag = False		# 同时, 将购买商品标志设为False, 结束该循环

                else:	# 若商品不存在, 给用户提示
                    buy_input_flag = True
                    print("\n商品不存在！！！")
                    continue	# 此处后不再向下执行，而是开始新的循环

            elif choice == "q" or choice == "Q": 	# 判断用户输入的字符是否，不是“数字”, 并且 为“q”或者“Q”
                Quit = True		# 将退出标志设为True
                go_shopping = False		# 将购物标志设为False , 即该次循环结束后，不在继续循环

            else:	# 当用户输入的字符 不是【“数字”、“Q”、“q”】之一时
                buy_input_flag = True	# 设购买标志为True （此处可不设，因为其值本身初始化为True，并且没有改变）
                print("\n商品不存在！！！")
                continue	# 此处后不再向下执行，而是开始新的循环

            if Quit:	# 如果退出标志被设置或改为True ，执行if下的子代码块
                input_quit = input("是否支付购物车内的商品？[Y/N]\n>>>")	# 接受用户命令

                if input_quit == "Y" or input_quit == "y":	# 接受到相应的命令
                    str2 = "<您已购买一下商品>"
                    print("\n", str2.center(40, "-"), end="")

                    for i in range(len(buy_git_num)):	# 循环遍历，打印用户选择的商品信息
                        print("\n\t{}、{}\t￥{}".format(i + 1, merchandise_info[i][0], merchandise_info[i][1]))
                        salary -= int(merchandise_info[i][1])	# 用户余额
                        print("\t剩余：%d"%(salary))

                        if salary <= 0:		# 资不抵债, 直接退出
                            exit("剩余：  ￥%d\n余额不足！！！" % (salary,))

                else:	# 接受到的字符为非“Y”、“y”
                    str3 = "<您购物车中的商品>"
                    print("\n", str3.center(42, "-"), end="")
                    for i in range(len(buy_git_num)):		# 打印用户选择的商品（购物车）信息
                        print("\n\t{}、{}\t￥{}".format(i + 1, merchandise_info[i][0], merchandise_info[i][1]))

                print("\n\t您当前的余额为：  ￥%d"%(salary,))
                print("-"*46)
                print("\n\t\t\t\t欢迎下次光临!!!")
                go_shopping = False		# 同时将购物标志设为False，用于结束外层循环
                break	# 从此出跳出（结束）该层循环

            print("\n已加入  {}到您的购物车 ".format(merchandise_info[choice][0]))

if __name__ == '__main__':  # 主程序入口
    main()		# 调用
