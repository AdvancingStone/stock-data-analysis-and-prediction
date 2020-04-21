-- 北向沪股通深股通每天涨幅榜top10
-- 序号	代码	名称		最新价	涨跌幅	成交额	换手率	市盈率	总市值		交易所	dt2			dt
-- 1		002156	通富微电	24.71	10.02	32.76亿	11.67	1489.34	285.08亿	深证	2020-04-17	20200417

create table if not exists bx_day_rise_top10(
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
dt2 string comment 'date format yyyy-MM-dd',
what_day string comment '周几'
)comment '北向每天涨幅榜-沪股通和深股通Top10'
partitioned by (dt string comment 'date format yyyyMMdd')
row format delimited
fields terminated by '\t'
stored as textfile;


-- 北向沪股通深股通每天买卖成交量top10
-- 排名	代码	股票简称	收盘价		涨跌幅		深股通净买额	深股通买入金额	深股通卖出金额	深股通成交金额	交易所			dt2				dt
-- 1		600519	贵州茅台	1226.00		2.41		7507.36万		8.02亿			7.26亿			15.28亿			上证			2020-04-17	20200417

create table if not exists bx_day_volumn_top10(
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
dt2 string comment 'date format yyyy-MM-dd',
what_day string comment '周几'
) comment '北向每天成交量榜-沪股通和深股通Top10'
partitioned by (dt string comment 'date format yyyyMMdd')
row format delimited
fields terminated by '\t'
stored as textfile;