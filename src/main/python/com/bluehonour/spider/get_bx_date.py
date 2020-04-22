#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from chinese_calendar import is_workday
import datetime
from pathlib import Path
import sys
sys.path.append("/home/liushuai/git_project/stock_data_analysis_prediction/stock-data-analysis-and-prediction/src/main/python/")


# 使用以下三行代码可以不弹出界面，实现无界面爬取
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(executable_path='geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
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
        last_one_day = datetime.timedelta(days=1)
        today = datetime.datetime.strptime(start_date,'%Y%m%d').date()
        end_date = datetime.datetime.strptime(end_date,'%Y%m%d').date()
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
        save_file("/home/xxx/stock-data/北向买卖A股时间")
    finally:
        driver.quit()

