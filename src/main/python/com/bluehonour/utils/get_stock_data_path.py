#!/usr/bin/python
import sys
import os

from com.bluehonour.utils.readConfig import ReadConfig


def get_stock_data_path():
    config = ReadConfig()
    path = config.find_path("config.ini")
    config.__read__(path)
    stock_path = config.get_stock("path")
    if not os.path.exists(stock_path):
        os.makedirs(stock_path)
    return stock_path
