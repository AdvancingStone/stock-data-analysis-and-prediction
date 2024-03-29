#!/usr/bin/python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from chinese_calendar import is_workday
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils import *

driver = Utils.Utils.getDriver()
WAIT = WebDriverWait(driver, 10)

data_list = []


def save_file(path):
    path = Path(path)
    # 保存数据并打印数据
    with open(str(path), 'w', encoding='UTF-8') as f:  # a追加写入
        for i in data_list:
            f.write(i + '\n')
            print(i)
        f.close()


if __name__ == '__main__':
    try:
        start_date = '20200101'
        end_date = '20200111'
        last_one_day = timedelta(days=1)
        today = datetime.strptime(start_date,'%Y%m%d').date()
        end_date = datetime.strptime(end_date,'%Y%m%d').date()
        current_url = 'http://data.eastmoney.com/hsgt/top10.html'
        while today <= end_date:
            if is_workday(today):
                driver.get(current_url[:-5] + "/" + str(today) + ".html")
                page_load_complete = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".titbar > .tit")))
                # print("页面加载完成")
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                date = soup.select_one(".sitebody > .maincont > .contentBox > .content > .tab1")
                # print(today)
                data_list.append(today.strftime('%Y%m%d'))
                # print(date is not None)
            today = today+last_one_day
        path = get_stock_data_path()
        save_file(path+"/北向买卖A股时间")
    finally:
        driver.quit()

