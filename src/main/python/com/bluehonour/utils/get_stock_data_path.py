#!/usr/bin/python
import sys
import os
import shutil
from readConfig import *


def get_stock_data_path():
    config = ReadConfig()
    path = config.find_path("config.ini")
    config.__read__(path)
    stock_path = config.get_stock("path")
    if not os.path.exists(stock_path):
        os.makedirs(stock_path)
    return stock_path


def mkdir(directory):

    """
    如果directory不存在则创建，如果存在删除该目录下所有内容
    :param directory: 路径
    :return:
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
