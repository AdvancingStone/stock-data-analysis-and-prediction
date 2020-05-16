#!/usr/bin/python
from datetime import datetime


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
