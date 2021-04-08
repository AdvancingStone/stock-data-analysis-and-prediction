#!/usr/bin/python
from pathlib import Path
import os
import shutil

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

from readConfig import ReadConfig
from datetime import datetime


class Utils:
    """
    工具类
    """
    @staticmethod
    def save_file(file_name, row_list, mode):
        """
        将 row_list 中的股票数据保存到 file_name 路径文件中
        :param file_name: 路径文件名
        :param row_list: 存放股票数据的列表
        :param mode: 写入模式， w：覆盖写， a：追加
        :return:
        """
        path = Path(file_name)

        with open(str(path), mode, encoding='UTF-8') as f:  # a追加写入
            for i in row_list:
                row_result = ''
                for j in i:
                    result = j.replace("%", '')
                    row_result += ('\t' + result)
                f.write(row_result.lstrip() + '\n')
                print(row_result.lstrip())
            f.close()


    @staticmethod
    def save_date(file_name, data_list, mode):
        """
        写入日期
        :param path:
        :return:
        """
        path = Path(file_name)
        # 保存数据并打印数据
        with open(str(path), mode, encoding='UTF-8') as f:
            for i in data_list:
                f.write(i + '\n')
                print(i)
            f.close()

    @staticmethod
    def date2weekday(date):

        """
        接收一个 yyyyMMdd的日期，返回对应的星期
        :param date: yyyyMMdd
        :return: weekday
        """
        week = datetime.strptime(date,"%Y%m%d").weekday()
        return {
            0: "星期一",
            1: "星期二",
            2: "星期三",
            3: "星期四",
            4: "星期五",
            5: "星期六",
            6: "星期日"
        }.get(week)


    def print_title(title_list):
        """
        打印标题
        :return:
        """
        for i in title_list:
            print(i, end='\t')
        print()


    def get_stock_data_path():

        """
        :return: 保存股票数据的根路径
        """
        config = ReadConfig()
        path = config.find_path("config.ini")
        config.__read__(path)
        stock_path = config.get_stock("path")
        if not os.path.exists(stock_path):
            os.makedirs(stock_path)
        return stock_path

    @staticmethod
    def remkdir(directory):

        """
        如果directory不存在则创建，如果存在删除该目录下所有内容
        :param directory: 路径
        :return: 创建成功返回true， 否则false
        """
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            return True
        except Exception:
            return False

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

    def getDriver():
        """
        返回selenium的driver
        :return:
        """
        config = ReadConfig()
        path = config.find_path("config.ini")
        config.__read__(path)
        browser_path = config.get_browser("path")
        driver_path = config.get_driver("path")

        # self.driver = webdriver.Firefox()
        # self.driver.set_window_position(0, 0)
        # self.driver.set_window_size(1400, 900)
        # self.driver.maximize_window()  # 让窗口最大化

        # 使用以下三行代码可以不弹出界面，实现无界面爬取
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.binary_location = browser_path
        # chrome浏览器配置，添加options参数， executable_path 可选，配置了环境变量后可省略，不然传该驱动的绝对路径
        driver = webdriver.Chrome(executable_path=driver_path,
                                  options=options)
        # 火狐浏览器配置
        # driver = webdriver.Firefox(executable_path='geckodriver', options=options)
        return driver