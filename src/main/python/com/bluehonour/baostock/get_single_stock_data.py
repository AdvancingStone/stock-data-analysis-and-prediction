import baostock as bs
import pandas as pd
import sys
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import *


# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

stock_code = "sz.000002"
start_date = '2020-01-01'
end_date = '2020-1-31'

# 获取沪深A股历史K线数据
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
rs = bs.query_history_k_data_plus(stock_code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                  start_date=start_date, end_date=end_date,
                                  frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

# 结果集输出到csv文件
path = get_stock_data_path() + "/single_stock/"
if not os.path.exists(path):
    os.makedirs(path)
filename = path + "/" + stock_code + "-" + start_date.replace("-", "") + "-" + end_date.replace("-", "") + ".csv"
result.to_csv(filename, index=False)
print(result)

# 登出系统
bs.logout()
