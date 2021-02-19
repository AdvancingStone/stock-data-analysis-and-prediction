#!/usr/bin/python
import os
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# __file__获取执行文件相对路径，整行为取上一级的上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import Utils

"""
北向沪股通深股通涨幅榜top10
"""

# 创建一个存放标题的列表
title_list = []
# 创建一个存放股票数据的二维列表
row_list = []  # 行
column_list = []  # 列

# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# options.binary_location=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# 添加options参数， executable_path 可选，配置了环境变量后可省略，不然传该驱动的绝对路径
# driver = webdriver.Chrome(executable_path='chromedriver', options=options)# 配了环境变量第一个参数就可以省了，不然传绝对路径
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
driver.get("http://data.eastmoney.com/hsgt/index.html")
WAIT = WebDriverWait(driver, 10)


class BxDayRiseTop10:
    def get_stock_data(self, jys, path):
        """
        获取上证和深证交易所的北向买入涨幅前10的股票数据
        :param jys: 交易所
        :param path: 路径
        :return: 股票数据的绝对路径地址
        """
        if jys.__eq__("深证"):
            input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#zfb_filter > ul > li:nth-child(2)")))
            input.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        date = soup.select_one("#updateTime_bxzj").string
        dt2 = date  # yyyy-MM-dd
        dt = date.replace("-", "")  # yyyyMMdd
        weekday = Utils.Utils.date2weekday(dt)

        list = soup.find(class_='dataview-center').find(class_='dataview-body')

        if jys.__eq__("深证"):
            title_items = list.select("thead > tr")  # 获取标题
            for item in title_items:
                th_items = item.select("th")
                for th_item in th_items:
                    if th_item.string != '相关':
                        title_list.append(th_item.string)
                title_list.append('交易所')
                title_list.append("dt2")
                title_list.append("dt")
                title_list.append("weekday")

        global column_list
        content_items = list.select("tbody > tr")
        for tr_item in content_items:
            td_items = tr_item.select("td")
            for td_item in td_items:
                if td_item.string is not None:
                    column_list.append(td_item.string)
            column_list.append(jys)
            column_list.append(dt2)
            column_list.append(dt)
            column_list.append(weekday)

            row_list.append(column_list)
            column_list = []

        absolute_path = path + "/" + dt[:-2] + "/"
        if not os.path.isdir(absolute_path):
            os.makedirs(absolute_path)
        return absolute_path + dt

    def get_bx_day_rise_top10(self):
        try:
            path = Utils.Utils.get_stock_data_path() + '/bx_day_rise_top10'
            self.get_stock_data("上证", path)
            file_name = self.get_stock_data("深证", path)
            Utils.Utils.print_title(title_list)
            Utils.Utils.save_file(file_name, row_list, 'w')
        finally:
            driver.quit()


if __name__ == '__main__':

    try:
        path = Utils.Utils.get_stock_data_path() + '/bx_day_rise_top10'
        data = BxDayRiseTop10()
        data.get_stock_data("上证", path)
        file_name = data.get_stock_data("深证", path)
        Utils.Utils.print_title(title_list)
        Utils.Utils.save_file(file_name, row_list, 'w')
    finally:
        driver.quit()
