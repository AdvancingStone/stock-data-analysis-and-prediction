#!/usr/bin/python
import baostock as bs
import os
import sys
import shutil
from _datetime import datetime, timedelta
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#__file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utils import *


def mkdir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def get_pre_date(beforeOfDay, current_date='nothing'):
    if current_date.__eq__("nothing"):
        today = datetime.now()
    else:
        today = datetime.strptime(current_date, '%Y-%m-%d')
    # 计算偏移量
    offset = timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


class Downloader(object):
    def __init__(self,
                 output_dir,
                 date_start='1990-01-01',
                 date_end='2020-03-23'):
        self._bs = bs
        bs.login()
        self.date_start = date_start
        # self.date_end = datetime.now().strftime("%Y-%m-%d")
        self.date_end = date_end
        self.output_dir = output_dir
        self.fields = "date,code,open,high,low,close,volume,amount," \
                      "adjustflag,turn,tradestatus,pctChg,peTTM," \
                      "pbMRQ,psTTM,pcfNcfTTM,isST"

    def exit(self):
        bs.logout()

    def get_codes_by_date(self, date):
        print(date)
        stock_rs = bs.query_all_stock(date)
        stock_df = stock_rs.get_data()
        print(stock_df)
        return stock_df

    def run(self):
        stock_df = self.get_codes_by_date(self.date_end)
        for index, row in stock_df.iterrows():
            print(f'processing {row["code"]} {row["code_name"]}')
            df_code = bs.query_history_k_data_plus(row["code"], self.fields,
                                                   start_date=self.date_start,
                                                   end_date=self.date_end).get_data()
            df_code.to_csv(f'{self.output_dir}/{row["code"]}.{row["code_name"]}.csv', index=False)
        self.exit()


if __name__ == '__main__':
    # 获取前30天的股票数据
    # start_date = get_pre_date(10)
    # end_date = datetime.today().strftime('%Y-%m-%d')
    # while is_holiday(datetime.strptime(end_date,'%Y-%m-%d')):
    #     end_date = get_pre_date(1, end_date)
    #     print(end_date)

    # # 获取 [start_date, end_date] 全部股票的日K线数据
    # start_date = '2018-01-01'
    # end_date = '2020-04-21'

    print("请输入起始日期和结束日期，格式  yyyy-MM-dd")
    start_date = input("起始日期: ")
    end_date = input("结束日期: ")
    yearmonth = start_date[:7]

    print(start_date, end_date, yearmonth)
    # date_end必须是一个工作日，否则出现意想不到的结果
    path = get_stock_data_path() + '/all_stock_data_details/' + yearmonth
    mkdir(path)
    # print(path)
    downloader = Downloader(path, date_start=start_date, date_end=end_date)
    downloader.run()

