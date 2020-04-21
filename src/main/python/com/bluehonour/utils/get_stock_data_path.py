#!/usr/bin/python
import sys
sys.path.append("/home/liushuai/git_project/stock_data_analysis_prediction/stock-data-analysis-and-prediction/src/main/python/")
from com.bluehonour.utils.readConfig import ReadConfig
import os

def get_stock_data_path():
    config = ReadConfig()
    path = config.find_path("config.ini")
    config.__read__(path)
    stock_path = config.get_stock("path")
    if not os.path.exists(stock_path):
        os.makedirs(stock_path)
    return stock_path
