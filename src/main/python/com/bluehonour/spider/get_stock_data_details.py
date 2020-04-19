import baostock as bs
import os
import datetime
from chinese_calendar import is_holiday
from com.bluehonour.utils.get_stock_data_path import get_stock_data_path

OUTPUT = './stockdata'


def mkdir(directory):
    if not os.path.exists(directory):
            os.makedirs(directory)

# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def get_pre_date(beforeOfDay, current_date='nothing'):
    if current_date.__eq__("nothing"):
        today = datetime.datetime.now()
    else:
        today = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
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
        # self.date_end = datetime.datetime.now().strftime("%Y-%m-%d")
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
    start_date = get_pre_date(10)
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    while is_holiday(datetime.datetime.strptime(end_date,'%Y-%m-%d')):
        end_date = get_pre_date(1, end_date)
        print(end_date)

    # # 获取 [start_date, end_date] 全部股票的日K线数据
    # start_date = '2018-01-01'
    # end_date = '2020-04-17'

    print(start_date, end_date)
    # date_end必须是一个工作日，否则出现意想不到的结果
    path = get_stock_data_path
    downloader = Downloader(path, date_start=start_date, date_end=end_date)
    downloader.run()

