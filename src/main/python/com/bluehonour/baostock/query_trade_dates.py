import baostock as bs
import pandas as pd
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import *


"""
方法说明：通过API接口获取股票交易日信息，可以通过参数设置获取起止年份数据，提供上交所1990-今年数据。 
返回类型：pandas的DataFrame类型。

返回数据说明
参数名称	参数描述
calendar_date	日期
is_trading_day	是否交易日(0:非交易日;1:交易日)

例如：
calendar_date,is_trading_day
2020-05-01,0
"""

#### 登陆系统 ####
lg = bs.login()

print("请输入起始日期和结束日期，格式  yyyy-MM-dd")
start_date = input("起始日期: ")
end_date = input("结束日期: ")

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取交易日信息 ####
rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
print('query_trade_dates respond error_code:'+rs.error_code)
print('query_trade_dates respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

path = get_stock_data_path() + '/trade_dates/'
if not os.path.exists(path):
    os.makedirs(path)
filename = path + start_date.replace('-','') + '-' + end_date.replace('-', '')

#### 结果集输出到csv文件 ####
result.to_csv(filename, encoding="utf-8", index=False)
print(result)

#### 登出系统 ####
bs.logout()