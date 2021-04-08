# stock-data-analysis-and-prediction

根据北向和主力资金的行为分析和预测后市股票的涨跌




## 🕵️‍♀️ 开始准备

#### 下载浏览器驱动

| 浏览器  | 下载地址（选择对用的驱动程序下载）                           |
| :-----: | :----------------------------------------------------------- |
| Chrome  | https://sites.google.com/a/chromium.org/chromedriver/downloads |
|  Edge   | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Firefox | https://github.com/mozilla/geckodriver/releases              |
| Safari  | https://webkit.org/blog/6900/webdriver-support-in-safari-10/ |

#### 配置浏览器驱动

```bash
# 安装Firefox浏览器驱动，参考
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
# 下载完之后解压到某个文件夹下
tar -zxvf geckodriver-v0.26.0-linux64.tar.gz -C /opt/software/drivers
# 配置环境变量
vim /etc/profile
# 在文件最后面加入
DRIVERS_HOME=/opt/software/drivers
PATH=$PATH:$DRIVER_HOME
# 保存后使用source让环境变量立即生效
source /etc/profile
```

#### 环境安装

```bash
# 虚拟环境
virtualenv -p python3.7 venv
source ./venv/bin/activate
# 安装库依赖
pip install -r requirements.txt
# 退出虚拟环境
# deactivate 
```

#### 修改根目录下的config.ini

```ini
[stock]
# 股票数据存放路径
#path=/Volumes/SharedDisk/stock-data
path=D:/Volumes/SharedDisk/stock-data

[driver]
# 浏览器驱动绝对路径（以谷歌浏览器为例）
#path=/usr/local/software/drivers/chromedriver
path=D:/driver/chromedriver.exe

[browser]
# 浏览器绝对路径
#path=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
path=C:/Program Files/Google/Chrome/Application/chrome.exe

```



## 🕵️‍♀️股票数据获取

股票证券数据集来自于 [baostock](http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5)，一个免费、开源的证券数据平台，提供 Python API。

```bash
>> pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
```

| 说明                                       | 代码                                                         |
| ------------------------------------------ | ------------------------------------------------------------ |
| 所有股票数据细节                           | [get_stock_data_details.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/get_all_stock_data_details.py) |
| 北向每天涨幅榜top10                        | [bx_day_rise_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_day_rise_top10.py) |
| 北向每天买卖成交量top10                    | [bx_day_volume_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_day_volume_top10.py) |
| 北向历史成交量top10                        | [bx_history_volumn_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_history_volume_top10.py) |
| 北向买卖时间                               | [get_bx_behavior_date.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/get_bx_behavior_date.py) |
| 单个股票数据细节                           | [get_single_stock_data.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/get_single_stock_data.py) |
| 板块资金流                                 | [sector_fund_flow.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/sector_fund_flow.py) |
| 个股资金流                                 | [single_stock_fund_flow.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/single_stock_fund_flow.py) |
| 股票基本信息(股票代码、股票名称、交易状态) | [query_stock_basic_info.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/query_stock_basic_info.py) |
| 股票交易日信息                             | [query_trade_dates.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/query_trade_dates.py) |
| 当日龙虎榜信息                             | [dragon_tiger_list.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/dragon_tiger_list.py) |
| 历史龙虎榜信息                             | [history_dragon_tiger_list.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/history_dragon_tiger_list.py) |



## 🕵️‍♀️使用hive存放数据 

#### sql 表的创建 

执行根目录下 [create-table.sql](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/create-table.sql)

```
根目录下 sql/create-table.sql 
```

#### hive table说明

对于数据库表字段的表述参考[stock_table_description](./doc/stock_table_description.md)

```
根目录下 doc/stock_table_description.md
```

#### 将数据导入Hive

```bash
# 用法 local从本地导入，无local代表从hdfs导入；overwrite是否覆盖；partition分区导入
load data [local] inpath filepath [overwrite] into table tablename [partition (a1=a2,b1=b2,...)]

# 从本地导入
load data local inpath '/home/xxx/stock-data/details/2020-01' overwrite into table stock_details partition (yearmonth=202001);
# 从hdfs导入
load data inpath '/home/xxx/stock-data/details/2020-01' overwrite into table stock_details partition (yearmonth=202001);
```



## 🕵️‍♀️股票数据分析

- [北向每月流入涨幅榜单汇总](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%B6%A8%E5%B9%85%E6%A6%9C%E5%8D%95%E6%B1%87%E6%80%BB.sql)
- [北向每月流入成交量榜单汇总](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%88%90%E4%BA%A4%E9%87%8F%E6%A6%9C%E5%8D%95%E6%B1%87%E6%80%BB.sql)
- [北向每月流入成交量股票明细](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%88%90%E4%BA%A4%E9%87%8F%E8%82%A1%E7%A5%A8%E6%98%8E%E7%BB%86.sql)
- [北向涨幅和成交量榜top10汇总](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/bx_top10_smmary.sql)
- [龙虎榜汇总](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/dragon_tiger_list_aggregate_analyze.sql)
- [龙虎榜上榜条件分析](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/dragon_tiger_list_condition_analyze.sql)
