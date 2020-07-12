#!/usr/bin/python
import os
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)
from utils import Utils


class HistoryDragonTigerList():
    """
    龙虎榜
    """

    def __init__(self):
        # 创建一个存放标题的列表
        self.title_list = []
        # 创建一个存放股票数据的二维列表
        self.row_list = []  # 行
        self.column_list = []  # 列

        # self.driver = webdriver.Firefox()
        # self.driver.set_window_position(0, 0)
        # self.driver.set_window_size(1400, 900)
        # self.driver.maximize_window()  # 让窗口最大化

        # 使用以下三行代码可以不弹出界面，实现无界面爬取
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Firefox(executable_path='geckodriver', options=self.options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

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

    def update_date_range(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        remove_start_date = 'document.getElementsByClassName("date-input")[0].removeAttribute("readonly");'
        self.driver.execute_script(remove_start_date)
        add_start_date = 'document.getElementsByClassName("date-input")[0].value="' + start_date + '"'
        self.driver.execute_script(add_start_date)

        remove_end_date = 'document.getElementsByClassName("date-input")[1].removeAttribute("readonly");'
        self.driver.execute_script(remove_end_date)
        add_end_date = 'document.getElementsByClassName("date-input")[1].value="' + end_date + '"'
        self.driver.execute_script(add_end_date)

        query_elem = '//*[@id="divSjri"]/div[2]/div[2]'
        self.load_page_by_xpath(self.WAIT, query_elem).click()
        time.sleep(8)
        print("时间修改完毕"+start_date+"\t"+end_date)

    def analysis_page_source(self, html, filename):
        """
        解析网页
        :param filename:
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'lxml')
        date_elem = soup.select_one("#search_date_start")
        year = str(date_elem.attrs["value"]).replace('-', '')[0:4]
        # 获取标题信息
        title_items = soup.select_one('#tab-1 > thead').find("tr").find_all("th")
        for item in title_items:
            if item.text != '相关':
                self.title_list.append(str(item.text).strip())
        self.title_list.append("星期")
        Utils.Utils.print_title(self.title_list)
        self.title_list.clear()

        # 获取股票数据
        tr_elems = soup.select("#tab-1 > tbody > tr")
        for tr_elem in tr_elems:
            td_items = tr_elem.select("td")
            td_size = len(td_items)
            for i in range(0, td_size):
                if i == 17:
                    self.column_list.append(str(td_items[i].select_one('span').attrs['title']).strip())
                elif i == 4:
                        month_day = str(td_items[i].text).strip()
                        dt = year + month_day[0:2] + month_day[3:5]
                        self.column_list.append(dt)
                        weekday = Utils.Utils.date2weekday(dt)
                elif i != 3:
                    self.column_list.append(str(td_items[i].text).strip())

            self.column_list.append(weekday)
            self.row_list.append(self.column_list)
            self.column_list = []
        Utils.Utils.save_file(filename, self.row_list, 'a')
        self.row_list.clear()

    def get_current_window(self):
        """
        获取当前页面
        :return:
        """
        time.sleep(8)
        # 获取当前页面句柄
        current_window = self.driver.current_window_handle
        # 获取所有页面句柄
        all_Handles = self.driver.window_handles
        # 如果新的pay_window句柄不是当前句柄，用switch_to_window方法切换
        for new_window in all_Handles:
            if new_window != current_window:
                self.driver.switch_to.window(new_window)
        # 隐式等待n秒,解释JavaScript是需要时间的，如果短了就无法正常获取数据，如果长了浪费时间；
        # implicitly_wait()给定时间智能等待
        self.driver.implicitly_wait(10)


    def get_stock_data(self, path, start_date, end_date):
        """
        获取龙虎榜数据
        :param path: 文件保存路径
        :param start_date: yyyyMMdd
        :param end_date: yyyyMMdd
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = path + '/' + start_date + '-' + end_date
        if os.path.exists(file_name):
            print(file_name + " 文件已存在...\t退出")
            return
        self.driver.get(self.current_url)
        show_date_window_xpath = '//*[@id="divSjri"]/div[1]'
        self.load_page_by_xpath(self.WAIT, show_date_window_xpath).click()

        start_date = start_date[0:4] + "-" + start_date[4:6] + "-" + start_date[6:8]
        end_date = end_date[0:4] + "-" + end_date[4:6] + "-" + end_date[6:8]
        self.update_date_range(start_date, end_date)
        self.get_current_window()

        # 获取最大页面
        max_page_elem_xpath = "//*[@id='PageCont']/a[last()-2]"
        max_page_elem = self.load_page_by_xpath(self.WAIT, max_page_elem_xpath)

        max_page = str(max_page_elem.text).strip()
        print("最大页面", max_page)
        if max_page.__eq__("..."):
            max_page_elem.click()
            self.get_current_window()
            max_page_elem_xpath = "//*[@id='PageCont']/child::node()[last()-4]"
            max_page_elem = self.load_page_by_xpath(self.WAIT, max_page_elem_xpath)
            max_page_elem.click()
            max_page = str(max_page_elem.text).strip()
            print("最大页面", max_page)
            first_page_elem_xpath = "//*[@id='PageCont']/a[2]"
            self.load_page_by_xpath(self.WAIT, first_page_elem_xpath).click()

        max_page_num = int(max_page)

        for i in range(0, max_page_num):
            print("第", i+1, "页")
            self.get_current_window()
            html = self.driver.page_source
            self.analysis_page_source(html, file_name)
            # 获取下一页元素
            next_page = self.driver.find_element_by_xpath("//*[@id='PageCont']/a[last()-1]")
            next_page.click()

    def get_history_dragon_tiger_list(self, start_date, end_date):
        """
        接口调用
        :param start_date: yyyyMMdd
        :param end_date: yyyyMMdd
        :return:
        """
        try:
            path = Utils.Utils.get_stock_data_path() + '/history_dragon_tiger_list'
            self.get_stock_data(path, start_date, end_date)
        finally:
            self.driver.quit()


if __name__ == '__main__':
    try:
        path = Utils.Utils.get_stock_data_path() + '/history_dragon_tiger_list'
        dtl = HistoryDragonTigerList()
        start_date = input("please input start_date for format yyyyMMdd: ")
        end_date = input("please input end_date for format yyyyMMdd: ")
        dtl.get_history_dragon_tiger_list(start_date, end_date)
    finally:
        dtl.driver.quit()

