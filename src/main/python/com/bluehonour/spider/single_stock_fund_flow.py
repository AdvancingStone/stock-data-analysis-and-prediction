#!/usr/bin/python

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import sys
import os
#__file__获取执行文件相对路径，整行为取上一级的上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import Utils

"""
获取个股资金流信息
"""
# 创建一个存放标题的列表
title_list = []
# 创建一个存放行业资金流信息的二维列表
row_list = []  # 行
column_list = []  # 列

# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

driver.get("http://data.eastmoney.com/zjlx/dpzjlx.html")
WAIT = WebDriverWait(driver, 10)

class SingleStockFundFlow:
    """
    个股资金流
    """
    def get_single_stock_fund_flow_data(self, path):
        date = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#updateTime_2")))
        date = date.text.replace("-", "")
        weekday = Utils.Utils.date2weekday(date)
        yearmonth = date[:-2]
        print(date)
        path = path + "/" + yearmonth
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path + "/" + date
        if os.path.exists(filename):
            print(filename + " 文件已存在...")
            return

        driver.get("http://data.eastmoney.com/zjlx/detail.html")
        WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#PageCont")))
        # 获取下一页元素
        next_page = driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-1]")
        max_page_elem = driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-2]").get_attribute("textContent")
        # 获取最大页面
        max_page = int(str(max_page_elem).strip())
        print("共", max_page, "页数据")
        print("获取第1页")
        global column_list
        for i in range(0, max_page):
            if i != 0:
                print("获取第", i+1, "页数据")
                next_page.click()
                WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#PageCont")))
                next_page = driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-1]")
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            list = soup.find(class_='maincont').find(class_='tab1')

            if i==0:
                title_items = list.find(class_='h101').find_all('th')   #获取标题
                for item in title_items:
                    if item.string!='相关':
                        title_list.append(item.string)
                title_list.append('日期')
                title_list.append('星期')
                Utils.Utils.print_title(title_list)
                title_list.clear()


            content_items = list.select("tbody > tr")
            for tr_item in content_items:
                td_items = tr_item.select("td")
                for td_item in td_items:
                    if td_item.string is not None:
                        column_list.append(td_item.string)
                column_list.append(date)
                column_list.append(weekday)
                row_list.append(column_list)
                column_list = []

        Utils.Utils.save_file(filename, row_list, 'w')
        row_list.clear()

    def get_single_stock_fund_flow(self, path):
        try:
            self.get_single_stock_fund_flow_data(path)
        finally:
            driver.quit()


if __name__ == '__main__':

    try:
        path = Utils.Utils.get_stock_data_path() + '/single_stock_fund_flow'
        SingleStockFundFlow().get_single_stock_fund_flow(path)
    finally:
        driver.quit()
