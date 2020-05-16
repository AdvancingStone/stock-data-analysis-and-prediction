#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import sys
import os
sys.path.append("/home/liushuai/git_project/stock_data_analysis_prediction/stock-data-analysis-and-prediction/src/main/python/")
from com.bluehonour.utils.get_stock_data_path import get_stock_data_path
from pathlib import Path
from com.bluehonour.utils.date_to_weekday import date2weekday


"""
获取行业资金流信息
"""
# 创建一个存放标题的列表
title_list = []
# 创建一个存放行业资金流信息的二维列表
row_list = []  # 行
column_list = []  # 列

driver = webdriver.Chrome()
driver.set_window_position(0, 0)
driver.set_window_size(1400, 900)
driver.maximize_window()#让窗口最大化

# 使用以下三行代码可以不弹出界面，实现无界面爬取
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

driver.get("http://data.eastmoney.com/zjlx/dpzjlx.html")
WAIT = WebDriverWait(driver, 10)

def get_sector_fund_flow_data(path):
    date = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#updateTime_2")))
    date = date.text.replace("-", "")
    weekday = date2weekday(date)
    yearmonth = date[:-2]
    print(date)

    driver.get("http://data.eastmoney.com/bkzj/hy.html")
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#PageCont")))
    # 获取下一页元素
    next_page = driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-1]")
    max_page_elem = driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-2]").get_attribute("textContent")
    # 获取最大页面
    max_page = int(str(max_page_elem).strip())
    global column_list
    for i in range(0, max_page):
        if i != 0:
            next_page.click()
            WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#PageCont")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find(class_='maincont').find(class_='tab1')

        # title_items = list.find(class_='h101').find_all('th')   #获取标题
        # for item in title_items:
        #     if item.string!='相关':
        #         title_list.append(item.string)
        # title_list.append('日期')
        #
        # for i in title_list:
        #     print(i, end='\t')
        # print()
        # title_list.clear()

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

    path = path+"/"+yearmonth
    if not os.path.exists(path):
        os.makedirs(path)
    save_file(path+"/"+date)
    row_list.clear()


def save_file(path):
    path = Path(path)
    # if path.exists():
    #     os.remove(path)
    print('开始写入数据 ====> ')
    with open(str(path), 'w', encoding='UTF-8') as f:  # a追加写入
        for i in row_list:
            row_result = ''
            for j in i:
                result = j.replace("%", '')
                row_result += ('\t' + result)
            f.write(row_result.lstrip() + '\n')
            print(row_result.lstrip())
        f.close()


if __name__ == '__main__':

    try:
        path = get_stock_data_path() + '/sector_fund_flow'
        get_sector_fund_flow_data(path)
    finally:
        driver.quit()
