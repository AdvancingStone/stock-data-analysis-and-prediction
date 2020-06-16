#!/usr/bin/python
import os
import sys
from _datetime import datetime, timedelta

from bs4 import BeautifulSoup
from chinese_calendar import is_workday
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import Utils


# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

driver.get("http://data.eastmoney.com/hsgt/top10.html")
current_url = driver.current_url
WAIT = WebDriverWait(driver, 10)
date_list = []


class BxBehaviorDate:

    def get_stock_data(self):
        """
        获取北向买卖的日期
        :return:
        """
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        content_date = soup.select(".titbar > .tit")[1].string
        (content, date) = str(content_date).split()
        dt2 = date[1:-3] # yyyy-MM-dd
        dt = dt2.replace("-", "") # yyyyMMdd
        what_day = date[-3:-1] #周一
        print(dt2, dt, what_day)
        date_list.append(dt)


    def get_interval_range_data(self, start_date, end_date):
        """
        获取从 start_date 到 end_date 之间工作日的股票数据
        :param path: 保存路径
        :param start_date: 开始时间
        :param end_date: 结束时间
        """
        next_one_day = timedelta(days=1)
        start_date = datetime.strptime(start_date,'%Y%m%d').date()
        end_date = datetime.strptime(end_date,'%Y%m%d').date()

        while end_date >= start_date:
            # print(end_date)
            if is_workday(start_date):
                driver.get(current_url[:-5] + "/" + str(start_date) + ".html")
                self.get_stock_data()
            start_date = start_date + next_one_day

    def get_bx_behavior_date(self, start_date, end_date):
        """
        获取从 start_date 到 end_date 之间北向的行为日期
        :param start_date: 起始日期
        :param end_date: 结束=日期
        :return:
        """
        try:
            path = Utils.Utils.get_stock_data_path() + '/bx_behavior_date/'
            if not os.path.exists(path):
                os.makedirs(path)
            date_file = path + start_date + '-' + end_date
            if not os.path.exists(date_file):
                self.get_interval_range_data(start_date, end_date)
                Utils.Utils.save_date(date_file, date_list, 'w')
            else:
                print(start_date + ',' + end_date + " 北向日期已经存在")
        finally:
            driver.quit()

if __name__ == '__main__':
    try:
        print("请输入起始日期和结束日期，格式  yyyyMMdd")
        start_date = input("起始日期: ")
        end_date = input("结束日期: ")
        path = Utils.Utils.get_stock_data_path() + '/bx_behavior_date/'
        if not os.path.exists(path):
            os.makedirs(path)
        date_file = path+start_date+'-'+end_date
        if not os.path.exists(date_file):
            BxBehaviorDate().get_interval_range_data(start_date, end_date)
            Utils.Utils.save_date(date_file, date_list, 'w')
        else:
            print(start_date+','+end_date+" 北向日期已经存在")
    finally:
        driver.quit()
