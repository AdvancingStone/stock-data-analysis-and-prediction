from urllib import request
import re


def extract_stock_data(url, encoding="gb2312"):
    """
    抽取股票数据
    :param url:
    :param encoding: 默认gb2312
    :return: list(list)
    """
    # 发起请求
    req = request.Request(url)
    # 获取响应
    rsp = request.urlopen(req)
    res = rsp.read().decode("gb2312")
    stock_arr = res.split(";")
    stock_arr.pop()
    return stock_arr


def process_stock_data(stock_arr, index_arr):
    """
    对股票数据进行预处理，获取指定下标的数据
    :param stock_arr:
    :param index_arr:
    :return: list(list)
    """
    result_arr = []
    for stock in stock_arr:
        inner_arr = []
        start = stock.find("\"")
        end = stock.rfind("\"")
        rest = stock[start + 1:end]
        arr = rest.split("~")
        for x in range(len(arr)):
            if x in index_arr:
                if x == 0:  # fund stock data code index is 0, sh600685
                    match_res = re.match("^([sh|sz]{2})(\d{6})$", arr[x])
                    if match_res.group(1) == "sh":
                        arr[x] = "上证"
                    elif match_res.group(1) == "sz":
                        arr[x] = "深证"
                inner_arr.append(arr[x])
        result_arr.append(inner_arr)
    return result_arr


def merge_stock_data(stock_arr, stock_brr):
    """
    将两个二维数组进行拉链操作
    :param stock_arr: 二维数组
    :param stock_brr: 二维数组
    :return: list(tuple(list, list))
    """
    zip_arr = zip(stock_arr, stock_brr)
    return list(zip_arr)


def concat_code(*codes, prefix="", suffix=","):
    """
    根据前后缀拼接股票代码
    :param codes: 可变参数
    :param prefix: 默认”“
    :param suffix: 默认”,"
    :return: str
    """
    result = ""
    for index in range(len(codes)):
        result += (prefix + codes[index] + suffix)
    if len(suffix) > 0:
        result = result[0:-1]
    return result


def traverse_tuple(zip_list):
    """
    遍历tuple
    :param zip_list:
    :return:
    """
    for tuples in zip_list:
        result = ""
        for lists in tuples:
            for li in lists:
                result += (li + ",")
        print(result[0:-1])


def get_stock_real_time_data(*codes):
    # detail_url = 'http://qt.gtimg.cn/q=sh600584,sz000858,sh600582,sh600585'
    detail_url = "http://qt.gtimg.cn/q=" + concat_code(*codes)
    detail_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                    28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48]
    detail_data = extract_stock_data(detail_url)
    detail_arr = process_stock_data(detail_data, detail_index)

    # fund_url = 'http://qt.gtimg.cn/q=ff_sh600584,ff_sz000858,ff_sh600582,ff_sh600585'
    fund_url = 'http://qt.gtimg.cn/q=' + concat_code(*codes, prefix="ff_")
    fund_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13]
    fund_data = extract_stock_data(fund_url)
    fund_arr = process_stock_data(fund_data, fund_index)
    result = merge_stock_data(detail_arr, fund_arr)
    traverse_tuple(result)


if __name__ == '__main__':
    # get_stock_real_time_data("sh600584", "sz000858", "sh600585");
    get_stock_real_time_data("sh600307")

