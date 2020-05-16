#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from chinese_calendar import is_workday, is_holiday
import datetime
from pathlib import Path
import sys
import os
from com.bluehonour.utils.get_stock_data_path import get_stock_data_path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

driver.get("http://data.eastmoney.com/hsgt/top10.html")
current_url = driver.current_url
WAIT = WebDriverWait(driver, 10)
date_list = []


def get_stock_data():
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    content_date = soup.select(".titbar > .tit")[1].string
    (content, date) = str(content_date).split()
    dt2 = date[1:-3] # yyyy-MM-dd
    dt = dt2.replace("-", "") # yyyyMMdd
    what_day = date[-3:-1] #周一
    print(dt2, dt, what_day)
    date_list.append(dt)


def save_file(path):
    path = Path(path)
    # if path.exists():
    #     os.remove(path)
    print('开始写入数据 ====> ')
    # 打印标题
    for i in date_list:
        print(i)

    # 保存数据并打印数据
    with open(str(path), 'w', encoding='UTF-8') as f:  # a追加写入
        for i in date_list:
            f.write(i.strip() + '\n')
            print(i)
        f.close()


def get_interval_range_data(start_date, end_date):
    """
    获取从 start_date 到 end_date 之间工作日的股票数据
    :param path: 保存路径
    :param start_date: 开始时间
    :param end_date: 结束时间
    """
    pre_one_day = datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime(start_date,'%Y%m%d').date()
    today = datetime.datetime.strptime(end_date,'%Y%m%d').date()

    while today >= start_date:
        # print(today)
        if is_workday(today):
            driver.get(current_url[:-5] + "/" + str(today) + ".html")
            get_stock_data()
        today = today-pre_one_day


if __name__ == '__main__':
    try:
        path = get_stock_data_path() + '/bx_behavior_date'
        get_interval_range_data('20180101', '20200531')
        save_file(path)
    finally:
        driver.quit()
