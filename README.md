# stock-data-analysis-and-prediction

根据北向和主力资金的行为分析和预测后市股票的涨跌



### 股票具体细节

| 参数名称    | 参数描述         | 说明                                |
| ----------- | ---------------- | ----------------------------------- |
| date        | 交易所行情日期   | 格式：YYYY-MM-DD                    |
| code        | 证券代码         | 格式：sh.600000。sh：上海，sz：深圳 |
| open        | 今开盘价格       | 精度：小数点后4位；单位：人民币元   |
| high        | 最高价           | 精度：小数点后4位；单位：人民币元   |
| low         | 最低价           | 精度：小数点后4位；单位：人民币元   |
| close       | 今收盘价         | 精度：小数点后4位；单位：人民币元   |
| preclose    | 昨日收盘价       | 精度：小数点后4位；单位：人民币元   |
| volume      | 成交数量         | 单位：股                            |
| amount      | 成交金额         | 精度：小数点后4位；单位：人民币元   |
| adjustflag  | 复权状态         | 不复权、前复权、后复权              |
| turn        | 换手率           | 精度：小数点后6位；单位：%          |
| tradestatus | 交易状态         | 1：正常交易 0：停牌                 |
| pctChg      | 涨跌幅（百分比） | 精度：小数点后6位                   |
| peTTM       | 滚动市盈率       | 精度：小数点后6位                   |
| psTTM       | 滚动市销率       | 精度：小数点后6位                   |
| pcfNcfTTM   | 滚动市现率       | 精度：小数点后6位                   |
| pbMRQ       | 市净率           | 精度：小数点后6位                   |
| isST        | 是否ST           | 1是，0否                 |


## 🕵️‍♀️ 准备

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

#### 修改数据存放路径

```
修改根目录下的config.ini
存放股票有关数据的地方

[stock]
path=/home/xxx/stock-data
```



### 股票数据获取

股票证券数据集来自于 [baostock](http://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5)，一个免费、开源的证券数据平台，提供 Python API。

```bash
>> pip install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
```



股票数据细节获取代码参考 [get_stock_data_details.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/get_all_stock_data_details.py)

```bash
>> python get_all_stock_data_details.py
```

北向每天涨幅榜top10获取代码参考 [bx_day_rise_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_day_rise_top10.py)

```bash
>> python bx_day_rise_top10.py
```

北向每天买卖成交量top10获取代码参考 [bx_day_volume_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_day_volume_top10.py)

```bash
>> python bx_day_volume_top10.py
```

北向历史成交量top10获取代码参考 [bx_history_volumn_top10.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/bx_history_volume_top10.py)

```bash
>> python bx_history_volume_top10.py
```

北向买卖时间获取代码参考 [get_bx_behavior_date.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/get_bx_behavior_date.py)

```bash
>> python get_bx_behavior_date.py
```

获取单个股票数据 [get_single_stock_data.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/get_single_stock_data.py) 

```bash
>> python get_single_stock_data.py 
```

主力每天的板块资金流 [sector_fund_flow.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/sector_fund_flow.py)

```bash
>> python sector_fund_flow.py
```

获取股票基本信息(股票代码、股票名称、交易状态) [query_stock_basic_info.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/query_stock_basic_info.py)

```bash
>> python query_stock_basic_info.py
```

获取股票交易日信息  [query_trade_dates.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/baostock/query_trade_dates.py) 

```bash
>> python query_trade_dates.py
```

获取龙虎榜信息 [dragon_tiger_list.py](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/src/main/python/com/bluehonour/spider/dragon_tiger_list.py)

```bash
>> python dragon_tiger_list.py
```



### hive sql 表的创建 

执行根目录下 [create-table.sql](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/create-table.sql)

```
根目录下 sql/create-table.sql 
```



### 导入数据

```bash
# 用法 local从本地导入，无local代表从hdfs导入；overwrite是否覆盖；partition分区导入
load data [local] inpath filepath [overwrite] into table tablename [partition (a1=a2,b1=b2,...)]

# 从本地导入
load data local inpath '/home/xxx/stock-data/details/2020-01' overwrite into table stock_details partition (yearmonth=202001);
# 从hdfs导入
load data inpath '/home/xxx/stock-data/details/2020-01' overwrite into table stock_details partition (yearmonth=202001);
```



### 股票数据分析

- [北向每月流入涨幅榜单汇总.sql](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%B6%A8%E5%B9%85%E6%A6%9C%E5%8D%95%E6%B1%87%E6%80%BB.sql)
- [北向每月流入成交量榜单汇总.sql](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%88%90%E4%BA%A4%E9%87%8F%E6%A6%9C%E5%8D%95%E6%B1%87%E6%80%BB.sql)
- [北向每月流入成交量股票明细.sql](https://github.com/AdvancingStone/stock-data-analysis-and-prediction/blob/master/sql/%E5%8C%97%E5%90%91%E6%AF%8F%E6%9C%88%E6%B5%81%E5%85%A5%E6%88%90%E4%BA%A4%E9%87%8F%E8%82%A1%E7%A5%A8%E6%98%8E%E7%BB%86.sql)

​	