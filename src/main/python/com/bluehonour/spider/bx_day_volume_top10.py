#!/usr/bin/python

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import Utils

"""
北向每天买卖成交量前十
"""

# 创建一个存放标题的列表
title_list = []
# 创建一个存放股票数据的二维列表
row_list = []  # 行
column_list = []  # 列

driver = Utils.Utils.getDriver()
driver.get("http://data.eastmoney.com/hsgt/index.html")
WAIT = WebDriverWait(driver, 10)


class BxDayVolumeTop10:

    def get_stock_data(self, jys, path):
        """
        获取上证和深证交易所的北向成交量前10的股票数据
        :param jys: 交易所
        :param path: 路径
        :return: 股票数据的绝对路径地址
        """
        if jys.__eq__("深证"):
            input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#top10_filter > ul > li:nth-child(2)")))
            input.click()
            time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        date = soup.select_one("#updateTime_bxzj").string
        dt2 = date  # yyyy-MM-dd
        dt = date.replace("-", "")  # yyyyMMdd
        weekday = Utils.Utils.date2weekday(dt)
        list = soup.find(id="dataview_top10").find(class_='dataview-center').find(class_='dataview-body')
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

    def get_bx_day_volume_top10(self):
        try:
            path = Utils.Utils.get_stock_data_path() + '/bx_day_volume_top10'
            self.get_stock_data("上证", path)
            path = self.get_stock_data("深证", path)
            Utils.Utils.print_title(title_list)
            Utils.Utils.save_file(path, row_list, 'w')
        finally:
            driver.quit()


if __name__ == '__main__':
    try:
        path = Utils.Utils.get_stock_data_path() + '/bx_day_volume_top10'
        data = BxDayVolumeTop10()
        data.get_stock_data("上证", path)
        path = data.get_stock_data("深证", path)
        Utils.Utils.print_title(title_list)
        Utils.Utils.save_file(path, row_list, 'w')
    finally:
        driver.quit()
