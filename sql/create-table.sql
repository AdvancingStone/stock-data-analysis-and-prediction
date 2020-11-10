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

create table if not exists stock.bx_day_volume_top10(
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


-- 北向历史时间
create table if not exists stock.bx_action_date(
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

-- 个股资金流
--序号	代码	名称	收盘价	涨跌幅	主力净流入净额	主力净流入净占比	超大单净流入净额	超大单净流入净占比	大单净流入净额	大单净流入净占比	中单净流入净额	中单净流入净占比	小单净流入净额	小单净流入净占比	dt		weekday
--1		000100	TCL科技	6.96	3.88	5.67亿			10.05				6.37亿				11.29				-7000.35万		-1.24				-3.14亿			-5.56				-2.53亿			-4.48				20200721	星期二
create table if not exists stock.single_stock_fund_flow(
xh int comment '序号',
code string comment '代码',
name string comment '名称',
spj decimal(20, 4) comment '收盘价',
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
dt string comment 'date format yyyyMMdd',
weekday string comment '星期几'
) comment '个股资金流'
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

--每日龙虎榜
--序号	代码	名称	解读						收盘价	涨跌幅	龙虎榜净买额(万)	龙虎榜买入金额(万)	龙虎榜卖出金额(万)	龙虎榜成交金额(万)	市场总成交金额(万)	净买金额占总成交比	成交金额占总成交比	换手率	流通市值(亿)	上榜原因					dt			星期	
--1		000011	深物业A	3家机构买入，成功率46.32	16.83	10.00	3433.90				9058.07				5624.17				14682.24			60453.50			5.68				24.29				7.29	89				日振幅值达到15的前五只证券	20200617	星期三

create table if not exists stock.dragon_tiger_list(
xh int comment '序号',
code int comment '代码',
name string comment '名称',
jd string comment '解读',
spj decimal(20, 4) comment '收盘价',
zdf decimal(20, 4) comment '涨跌幅',
jme decimal(20, 4) comment '龙虎榜净买额(万)',
mrje decimal(20, 4) comment '龙虎榜买入金额(万)',
mcje decimal(20, 4) comment '龙虎榜卖出金额(万)',
cjje decimal(20, 4) comment '龙虎榜成交金额(万)',
sczcjje decimal(20, 4) comment '市场总成交金额(万)',
jmje_rate decimal(20, 4) comment '净买金额占总成交比',
cjje_rate decimal(20, 4) comment '成交金额占总成交比',
hsl decimal(20, 4) comment '换手率',
ltsz decimal(20, 4) comment '流通市值(亿)',
sbyy string comment '上榜原因',
dt string comment '日期',
weekday string comment '星期几'
)comment '龙虎榜'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;

--历史龙虎榜
--序号	代码	名称		上榜日		解读					收盘价	涨跌幅	龙虎榜净买额(万)	龙虎榜买入额(万)	龙虎榜卖出额(万)	龙虎榜成交额(万)	市场总成交额(万)	净买额占总成交比	成交额占总成交比	换手率	流通市值(亿)	上榜原因					上榜后1日	上榜后2日	上榜后5日	上榜后10日	星期	
--1		000030	富奥股份	20200603	1家机构卖出成功率48.91	6.55	-3.53	-2002				5860				7862				13723				44596				-4.49				30.77				3.92	115				日振幅值达到15的前五只证券	-0.92		-9.16		-14.66		-12.92		星期三
create table if not exists stock.history_dragon_tiger_list(
xh int comment '序号',
code int comment '代码',
name string comment '名称',
dt string comment '上榜日',
jd string comment '解读',
spj decimal(20, 4) comment '收盘价',
zdf decimal(20, 4) comment '涨跌幅',
jme decimal(20, 4) comment '龙虎榜净买额(万)',
mrje decimal(20, 4) comment '龙虎榜买入金额(万)',
mcje decimal(20, 4) comment '龙虎榜卖出金额(万)',
cjje decimal(20, 4) comment '龙虎榜成交金额(万)',
sczcjje decimal(20, 4) comment '市场总成交金额(万)',
jmje_rate decimal(20, 4) comment '净买金额占总成交比',
cjje_rate decimal(20, 4) comment '成交金额占总成交比',
hsl decimal(20, 4) comment '换手率',
ltsz decimal(20, 4) comment '流通市值(亿)',
sbyy string comment '上榜原因',
t1 decimal(20, 4) comment '上榜后1日涨跌幅',
t2 decimal(20, 4) comment '上榜后2日涨跌幅',
t5 decimal(20, 4) comment '上榜后5日涨跌幅',
t10 decimal(20, 4) comment '上榜后10日涨跌幅',
weekday string comment '星期几'
)comment '历史龙虎榜'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;

--北向成交量和涨幅榜top10汇总
--增量，需要上月北向净买额数据（从2019年起开始计算）
create table if not exists stock.bx_top10_smmary(
code string comment '股票代码',
name string comment '股票名称',
history_jme decimal(20, 4) comment '北向历史净买额',
month_jme decimal(20, 4) comment '北向本月净买额',
time int comment '本月买卖次数',
max_zdf decimal(20, 4) comment '最大涨跌幅',
min_zdf decimal(20, 4) comment '最小涨跌幅',
month_zdf decimal(20, 4) comment '本月涨跌幅',
classify string comment '分类',
-- date_set array<string> comment '日期集'
date_set string comment '日期集'
)comment '北向成交量和涨幅榜top10汇总'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
collection items terminated by ';'
stored as textfile;

--龙虎榜汇总分析
create table if not exists stock.dragon_tiger_list_aggregate_analyze(
code string comment '股票代码', 
name string comment '股票名称',
dt string comment '上榜日',
is_rise string comment '是否涨跌',
trade_type string comment '交易类型',
funding_source string comment '资金来源',
jd string comment '解读',
spj decimal(20, 4) comment'收盘价',
zdf decimal(20, 4) comment '涨跌幅',
jme decimal(20, 4) comment '龙虎榜净买额(万)',
mrje decimal(20, 4) comment '龙虎榜买入金额(万)',
mcje decimal(20, 4) comment '龙虎榜卖出金额(万)',
cjje decimal(20, 4) comment '龙虎榜成交金额(万)',
sczcjje decimal(20, 4) comment '市场总成交金额(万)',
jmje_rate decimal(20, 4) comment '净买金额占总成交比',
cjje_rate decimal(20, 4) comment '成交金额占总成交比',
hsl decimal(20, 4) comment '换手率',
ltsz decimal(20, 4) comment '流通市值(亿)',
sbyy string comment '上榜原因',
zdf_t1 decimal(20, 4) comment '上榜后1日涨跌幅',
zdf_t2 decimal(20, 4) comment '上榜后2日涨跌幅',
zdf_t5 decimal(20, 4) comment '上榜后5日涨跌幅',
zdf_t10 decimal(20, 4) comment '上榜后10日涨跌幅',
weekday string comment '星期几'
)comment '龙虎榜成交量和涨幅榜top10汇总分析'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;

--龙虎榜上榜条件
create table if not exists stock.dragon_tiger_list_condition(
condition string comment '上榜条件'
);

--龙虎榜条件分析
create table if not exists stock.dragon_tiger_list_condition_analyze(
condition string comment '上榜条件',
funding_source string comment '资金来源',
trade_type string comment '交易类型',
total_time int comment '上榜总次数',
t1_rise_time int comment 'T+1个交易日上涨次数',
t2_rise_time int comment 'T+2个交易日上涨次数',
t5_rise_time int comment 'T+5个交易日上涨次数',
t10_rise_time int comment 'T+10个交易日上涨次数',
t1_rise_frequency decimal(10, 2) comment 'T+1个交易日上涨频率',
t2_rise_frequency decimal(10, 2) comment 'T+1个交易日上涨频率',
t5_rise_frequency decimal(10, 2) comment 'T+1个交易日上涨频率',
t10_rise_frequency decimal(10, 2) comment 'T+1个交易日上涨频率'
)comment '龙虎榜上榜原因'
partitioned by (yearmonth string comment '分区年月 format yyyyMM')
row format delimited
fields terminated by '\t'
stored as textfile;
