#!/usr/bin/python
import os
import sys
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from chinese_calendar import is_workday
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#__file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utils import Utils


"""
北向历史成交量前十
"""

# 创建一个存放标题的列表
title_list = []
# 创建一个存放股票数据的二维列表
row_list = []  # 行
column_list = []  # 列
# 北向买卖A股的时间列表
data_list = []

# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# options.binary_location=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# 添加options参数， executable_path 可选，配置了环境变量后可省略，不然传该驱动的绝对路径
# driver = webdriver.Chrome(executable_path='chromedriver', options=options)# 配了环境变量第一个参数就可以省了，不然传绝对路径
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
current_url = "http://data.eastmoney.com/hsgt/top10.html"
WAIT = WebDriverWait(driver, 10)


class BxHistoryVolumeTop10:

    def get_stock_data(self, path):
        for index in range(0, 2):
            page_load_complete = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".titbar > .tit")))
            print("页面加载完成")
            if index == 0:
                jys = "上证"
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                content_date = soup.select(".titbar > .tit")[1].string
                (content, date) = str(content_date).split()
                dt2 = date[1:-3] # yyyy-MM-dd
                dt = dt2.replace("-", "") # yyyyMMdd
                weekday = Utils.Utils.date2weekday(dt)
                print(dt2, dt, weekday)
            else:
                jys = "深证"

            list = soup.select(".sitebody > .maincont > .contentBox > .content > .tab1")[index]
            # 写入时间
            if index == 0:
                data_list.append(dt)

            title_items = list.find(class_='h101').find_all('th')   #获取标题
            for item in title_items:
                if '相关' not in item.string:
                    title_list.append(item.text)
            title_list.append("交易所")
            title_list.append("dt2")
            title_list.append("dt")
            title_list.append("周几")

            global column_list
            content_items = list.select("tbody > tr")
            # print(content_items)
            for tr_item in content_items:
                td_items = tr_item.select("td")
                for td_item in td_items:
                    item = str(td_item.get_text()).strip()
                    if "成交" not in item:
                        column_list.append(item)
                column_list.append(jys)
                column_list.append(dt2)
                column_list.append(dt)
                column_list.append(weekday)
                if column_list.__len__() > 5:  # 除去非周末的节假日
                    row_list.append(column_list)
                column_list = []
            if row_list:  # row_list是否含有元素
                # save_file(path)
                Utils.Utils.print_title(title_list)
                title_list.clear()
                Utils.Utils.save_file(path, row_list, 'a')
                row_list.clear()


    def get_latest_days_data(self, path, date_interval_days=30):
        """
        获取最近 date_interval_days 天的股票数据,默认30天
        :param path: 保存路径
        :param date_interval_days: 过去多少天
        :return:
        """
        today = datetime.date.today()
        pre_one_day = timedelta(days=1)
        for i in range(0, date_interval_days):
            if is_workday(today):
                driver.get(current_url[:-5] + "/" + str(today) + ".html")
                self.get_stock_data(path)
            today = today-pre_one_day


    def get_interval_range_data(self, path, start_date, end_date):
        """
        获取从 start_date 到 end_date 之间工作日的股票数据
        :param path: 保存路径
        :param start_date: 开始时间
        :param end_date: 结束时间
        """
        last_one_day = timedelta(days=1)
        today = datetime.strptime(start_date,'%Y%m%d').date()
        end_date = datetime.strptime(end_date,'%Y%m%d').date()

        while end_date >= today:
            print(today)
            if is_workday(today):
                driver.get(current_url[:-5] + "/" + str(today) + ".html")
                self.get_stock_data(path)
            today = today + last_one_day

    def get_bx_history_volume_top10(self, start_date, end_date):
        """
        获取 start_date 到 end_date 北向的历史成交量top10的股票数据
        :param start_date: 起始日期
        :param end_date: 结束日期
        :return:
        """
        try:
            stock_root_path = Utils.Utils.get_stock_data_path()
            yearmonth = start_date[:6]
            path = stock_root_path + '/bx_history_volume/'
            if not os.path.exists(path):
                os.makedirs(path)
            file_path = path + start_date + "-" + end_date
            if not os.path.exists(file_path):
                self.get_interval_range_data(file_path, start_date, end_date)
            # get_latest_days_data(path, 30)

            # 输出北向时间
            date_path = stock_root_path + '/bx_history_date/'
            if not os.path.exists(date_path):
                os.makedirs(date_path)
            date_path = date_path + start_date + "-" + end_date
            if not os.path.exists(date_path):
                Utils.Utils.save_date(date_path, data_list, 'w')
            else:
                print(start_date + '-' + end_date + ' 北向的历史数据已存在')
        finally:
            driver.quit()

if __name__ == '__main__':
    try:
        stock_root_path = Utils.Utils.get_stock_data_path()
        hist_data = BxHistoryVolumeTop10()
        print("请输入起始日期和结束日期，格式  yyyyMMdd")
        start_date = input("起始日期: ")
        end_date = input("结束日期: ")
        yearmonth = start_date[:6]
        path = stock_root_path + '/bx_history_volume/'
        if not os.path.exists(path):
            # shutil.rmtree(path=path)
            os.makedirs(path)
        file_path = path + start_date + "-" + end_date
        if not os.path.exists(file_path):
            hist_data.get_interval_range_data(file_path, start_date, end_date)
        # get_latest_days_data(path, 30)

        # 输出北向时间
        date_path = stock_root_path + '/bx_history_date/'
        if not os.path.exists(date_path):
            os.makedirs(date_path)
        date_path = date_path + start_date + "-" + end_date
        if not os.path.exists(date_path):
            Utils.Utils.save_date(date_path, data_list, 'w')
        else:
            print(start_date+'-'+end_date+' 北向的历史数据已存在')
    finally:
        driver.quit()
