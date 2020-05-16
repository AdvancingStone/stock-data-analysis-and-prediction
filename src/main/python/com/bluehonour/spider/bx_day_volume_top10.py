#!/usr/bin/python
from com.bluehonour.utils.get_stock_data_path import get_stock_data_path
from com.bluehonour.utils.date_to_weekday import date2weekday
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import sys,os
from pathlib import Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)



"""
北向每天买卖成交量前十
"""


# 创建一个存放标题的列表
title_list = []
# 创建一个存放股票数据的二维列表
row_list = []  # 行
column_list = []  # 列
# 获取当前日期和时间
# now_time = datetime.datetime.now()
# dt2 = now_time.strftime('%Y-%m-%d')  # yyyy-MM-dd
# dt = now_time.strftime('%Y%m%d')  # yyyyMMdd

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


def get_stock_data(jys, path):
    if jys.__eq__("深证"):
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mk_sdcjg > #SGT_3")))
        print(input.text)
        input.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    date = soup.select_one("#inputDate").string
    dt2 = date # yyyy-MM-dd
    dt = date.replace("-", "") # yyyyMMdd
    weekday = date2weekday(dt)

    list = soup.find_all(class_='maincont')[2].find(class_='tab1')

    title_items = list.find(class_='h101').find_all('th')   #获取标题
    for item in title_items:
        if '相关' not in item.text:
            title_list.append(item.text)
    title_list.append("交易所")
    title_list.append("dt2")
    title_list.append("dt")
    title_list.append("weekday")

    for i in title_list:
        print(i, end='\t')
    print()
    title_list.clear()

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
    save_file(path)
    row_list.clear()


for i in row_list:
    for j in i:
        result = j.replace("%", '')
        print(result, end='\t')
    print()


def save_file(path):
    path = Path(path)
    # if path.exists():
    #     os.remove(path)
    print('开始写入数据 ====> ')
    with open(str(path), 'a', encoding='UTF-8') as f:  # a追加写入
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
        path = get_stock_data_path() + '/bx_day_volume_top10'
        get_stock_data("上证", path)
        get_stock_data("深证", path)
    finally:
        driver.quit()
