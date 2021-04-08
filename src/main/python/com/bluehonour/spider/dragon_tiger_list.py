#!/usr/bin/python
import os
import sys
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utils import Utils


class DragonTigerList():
    """
    龙虎榜
    """

    def __init__(self):
        # 创建一个存放标题的列表
        self.title_list = []
        # 创建一个存放股票数据的二维列表
        self.row_list = []  # 行
        self.column_list = []  # 列

        self.driver = Utils.Utils.getDriver()
        self.current_url = "http://data.eastmoney.com/stock/tradedetail.html"
        self.WAIT = WebDriverWait(self.driver, 10)

    def load_page_by_xpath(self, web_driver_wait, xpath_elem):
        """
        通过selenium的xpath加载页面元素
        :param web_driver_wait:
        :param xpath_elem:
        :return: 被加载的元素
        """
        load_elem = web_driver_wait.until(EC.presence_of_element_located((By.XPATH, xpath_elem)))
        return load_elem

    def get_stock_data(self, path):
        """
        获取龙虎榜数据
        :param path: 文件保存路径
        :return:
        """
        self.driver.get(self.current_url)
        xpath = '//*[@id="divSjri"]/div[1]'
        self.load_page_by_xpath(self.WAIT, xpath).click()
        time.sleep(10)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        date_elem = soup.select_one("#search_date_start")
        year = str(date_elem.attrs["value"]).replace('-', '')[0:4]
        date = str(soup.select_one("#divSjri > ul > li:nth-child(1)").text).strip()
        dt = year + date[0:2] + date[3:5]
        weekday = Utils.Utils.date2weekday(dt)
        yearmonth = dt[:-2]
        path = path + "/" + yearmonth
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path + "/" + dt
        if os.path.exists(filename):
            print(filename + " 文件已存在...")
            return

        # 获取标题信息
        title_items = soup.select_one('#tab-1 > thead').find("tr").find_all("th")
        for item in title_items:
            if item.text != '相关':
                self.title_list.append(str(item.text).strip())
        self.title_list.append("dt")
        self.title_list.append("星期")
        Utils.Utils.print_title(self.title_list)
        self.title_list.clear()

        # 获取股票数据
        tr_elems = soup.select("#tab-1 > tbody > tr")
        for tr_elem in tr_elems:
            td_items = tr_elem.select("td")
            td_size = len(td_items)
            for i in range(0, td_size):
                if i == 16:
                    self.column_list.append(str(td_items[i].select_one('span').attrs['title']).strip())
                elif i != 3:
                    self.column_list.append(str(td_items[i].string).strip())
            self.column_list.append(dt)
            self.column_list.append(weekday)
            self.row_list.append(self.column_list)
            self.column_list = []
        Utils.Utils.save_file(filename, self.row_list, 'w')
        self.row_list.clear()

    def get_dragon_tiger_list(self):
        try:
            path = Utils.Utils.get_stock_data_path() + '/dragon_tiger_list'
            self.get_stock_data(path)
        finally:
            self.driver.quit()


if __name__ == '__main__':
    try:
        path = Utils.Utils.get_stock_data_path() + '/dragon_tiger_list'
        dtl = DragonTigerList()
        dtl.get_stock_data(path)
    finally:
        dtl.driver.quit()
        print()
