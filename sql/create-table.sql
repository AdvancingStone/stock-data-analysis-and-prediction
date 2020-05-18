-- 北向沪股通深股通每天涨幅榜top10
-- 序号	代码	名称		最新价	涨跌幅	成交额	换手率	市盈率	总市值		交易所	dt2			dt		weekday
-- 1	002156	通富微电	24.71	10.02	32.76亿	11.67	1489.34	285.08亿	深证	2020-04-17	20200417

create table if not exists stock.bx_day_rise_top10(
xh int comment '序号',
code int comment '代码',
name string comment '名称',
zxj decimal(10, 2) comment '最新价',
zdf decimal(10, 2) comment '涨跌幅(%)',
cje string comment '成交额',
hsl decimal(10, 2) comment '换手率(%)',
syl decimal(10, 2) comment '市盈率',
zsz string comment '总市值',
jys string comment '交易所(上海、深圳)',
dt2 date comment 'date format yyyy-MM-dd',
dt string comment 'date format yyyyMMdd',
weekday string comment '周几'
)comment '北向每天涨幅榜-沪股通和深股通Top10'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;


-- 北向沪股通深股通每天买卖成交量top10
-- 排名	代码	股票简称	收盘价		涨跌幅		深股通净买额	深股通买入金额	深股通卖出金额	深股通成交金额	交易所			dt2			dt		weekday
-- 1	600519	贵州茅台	1226.00		2.41		7507.36万		8.02亿			7.26亿			15.28亿			上证			2020-04-17	20200417

create table if not exists stock.bx_day_volumn_top10(
xh int comment '序号',
code int comment '代码',
name string comment '名称',
spj string comment '收盘价',
zdf decimal(10, 2) comment '涨跌幅(%)',
jme string comment '净买额',
mrje string comment '买入金额',
mcje string comment '卖出金额',
cjje string comment '成交金额',
jys string comment '交易所(上海、深圳)',
dt2 date comment 'date format yyyy-MM-dd',
dt string comment 'date format yyyyMMdd',
weekday string comment '周几'
) comment '北向每天成交量榜-沪股通和深股通Top10'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;


-- 股票具体细节
--date,		code,		open,		high,		low,		close,	volume,		amount,			adjustflag,	turn,		tradestatus,	pctChg,		peTTM,		pbMRQ,		psTTM,		pcfNcfTTM,		isST
--2018-01-02,	sz.000837,	6.1600,		6.2100,		6.1200,		6.2000,	3858021,	23835303.9600,	3,			0.662189,	1,				1.307188,	88.561479,	1.523950,	1.428011,	-747.210356,	0
--2020-04-21, sz.000837,	3.9900,		4.0100,		3.9000,		3.9100,	5277402,	20749013.8200,	3,			0.761400,	1,				-2.005000,	-9.111043,	1.062674,	0.856588,	-275.187176,	0

create table if not exists stock.stock_details(
dt date comment '交易所行情日期 (格式：YYYY-MM-DD)',
code string comment '证券代码 (格式：sh.600000。sh：上海，sz：深圳)',
open decimal(20, 4) comment '今开盘价格 (精度：小数点后4位；单位：人民币元)',
high decimal(20, 4) comment '最高价 (精度：小数点后4位；单位：人民币元)',
low decimal(20, 4) comment '最低价 (精度：小数点后4位；单位：人民币元)',
close decimal(20, 4) comment '今收盘价	(精度：小数点后4位；单位：人民币元)',
--preclose decimal(20, 4) comment '昨日收盘价 (精度：小数点后4位；单位：人民币元)',
volume bigint comment '成交数量 (单位：股)',
amount decimal(20, 4) comment '成交金额 (精度：小数点后4位；单位：人民币元)',
adjustflag tinyint comment '复权类型 (默认不复权：3；1：后复权；2：前复权)',
turn decimal(20, 4) comment '换手率 (精度：小数点后6位；单位：%		[指定交易日的成交量(股)/指定交易日的股票的流通股总股数(股)]*100%)',
tradestatus tinyint comment '交易状态 (1：正常交易   0：停牌)',
pctChg decimal(20, 4) comment '涨跌幅[百分比] (精度：小数点后6位；单位：%)	日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%',
peTTM decimal(20, 4) comment '滚动市盈率 (精度：小数点后6位)	(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM',
pbMRQ decimal(20, 4) comment '市净率 (精度：小数点后6位)		(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)',
psTTM decimal(20, 4) comment '滚动市销率 (精度：小数点后6位)	(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM',
pcfNcfTTM decimal(20, 4) comment '滚动市现率 (精度：小数点后6位)		(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM',
isST tinyint comment '是否ST股，1是，0否'
)comment '股票具体细节'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by ','
stored as textfile
tblproperties("skip.header.line.count"="1");

-- 导入数据
-- load data local inpath '/home/liushuai/stock-data/details/2020-01' overwrite into table stock_details partition (yearmonth=202001);
-- load data local inpath '/home/liushuai/stock-data/details/2020-02'  into table stock_details partition (yearmonth=202002);

-- 北向历史时间
create table if not exists bx_action_date(
dt string comment 'date format yyyyMMdd'
)comment '北向买卖A股的时间';


-- 主力每天板块资金流
--序号	板块名称	涨跌幅	主力净流入净额	主力净流入净占比	超大单净流入净额	超大单净流入净占比	大单净流入净额	大单净流入净占比	中单净流入净额	中单净流入净占比	小单净流入净额	小单净流入净占比	主力净流入最大股	date
--1		电子元件	1.19	18.61亿			1.79				27.49亿				2.65				-8.88亿			-0.86				-18.93亿		-1.83				3184.44万		0.03				兆易创新			20200515
create table if not exists stock.sector_fund_flow(
xh int comment '序号',
sector_name string comment '板块名称',
zdf decimal(10, 2) comment '涨跌幅(%)',
zljlrje string comment '主力净流入净额',
zljlrjzb decimal(10, 2) comment '主力净流入净占比(%)',
cddjlrje string comment '超大单净流入净额',
cddjlrjzb decimal(10, 2) comment '超大单净流入净占比(%)',
ddjlrje string comment '大单净流入净额',
ddjlrjzb decimal(10, 2) comment '大单净流入净占比(%)',
zdjlrje string comment '中单净流入净额',
zdjlrjzb decimal(10, 2) comment '中单净流入净占比(%)',
xdjlrje string comment '小单净流入净额',
xdjlrjzb decimal(10, 2) comment '小单净流入净占比(%)',
zljlrzdg string comment '主力净流入最大股',
dt string comment 'date format yyyyMMdd',
weekday string comment '星期几'
) comment '主力每天板块资金流'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;

-- 交易日查询，判断每个自然日是不是交易日(1表示交易日，0表示非交易日)
-- calendar_date,is_trading_day
-- 2020-05-01,0
create table if not exists stock.trade_dates(
calendar_date date comment '自然日',
is_trading_day char(1) comment '是否是交易日(1：交易日，0：非交易日)'
) comment '交易日信息，判断每个自然日是不是交易日'
row format delimited
fields terminated by ','
stored as textfile
tblproperties("skip.header.line.count"="1");

--获取股票基本信息，包括证券代码，证券名称，交易状态
create table if not exists stock.stock_basic_info(
code string comment '证券代码（sh.000001）',
tradeStatus char(1) comment '交易状态(1：正常交易 0：停牌）',
code_name string comment '证券名称（上证综合指数）'
) comment '股票基本信息'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by ','
stored as textfile
tblproperties("skip.header.line.count"="1");
