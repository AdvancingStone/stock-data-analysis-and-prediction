import baostock as bs
import pandas as pd
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import *


"""
方法说明：获取指定日期所有股票列表。
通过API接口获取证券代码及股票交易状态信息，与日K线数据同时更新。
可以通过参数‘某交易日’获取数据（包括：A股、指数），提供2006-今数据。 
返回类型：pandas的DataFrame类型


返回数据说明
参数名称	参数描述
code	证券代码    
tradeStatus	交易状态(1：正常交易 0：停牌）
code_name	证券名称

例如：
code,tradeStatus,code_name
sh.000001,1,上证综合指数
"""


#### 登陆系统 ####
lg = bs.login()

print("请输入起始日期和结束日期，格式  yyyy-MM-dd")
start_date = input("起始日期: ")
end_date = input("结束日期: ")

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取证券信息 ####
rs = bs.query_all_stock(day="2017-06-30")
print('query_all_stock respond error_code:'+rs.error_code)
print('query_all_stock respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

path = get_stock_data_path() + '/stock_basic_info/'
if not os.path.exists(path):
    os.makedirs(path)
filename = path + start_date.replace('-','') + '-' + end_date.replace('-', '')

#### 结果集输出到csv文件 ####
result.to_csv(filename, encoding="utf-8", index=False)
print(result)

#### 登出系统 ####
bs.logout()