#!/usr/bin/python
import os
import sys
import configparser


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()

    def __read__(self, configPath):
        self.cf.read(configPath)

    def get_stock(self, param):
        value = self.cf.get("stock", param)
        return value

    def get_separator(self):
        if 'win' in sys.platform:
            separator = '\\'
        else:
            separator = '/'
        return separator

    def find_path(self, file):
        o_path = os.getcwd()
        separator = self.get_separator()
        str = o_path.split(separator)
        while len(str) > 0:
            spath = separator.join(str)+separator+file
            leng = len(str)
            if os.path.exists(spath):
                return spath
            str.remove(str[leng-1])
        return str


if __name__ == '__main__':
    config = ReadConfig()
    path = config.find_path("config.ini")
    config.__read__(path)
    stock_path = config.get_stock('path')
    print(stock_path)
