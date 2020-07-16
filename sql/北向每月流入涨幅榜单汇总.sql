set hivevar:yearmonth='202006';
--北向每月流入涨幅榜单汇总
select
	code as `股票代码`,
	name as `股票名称`,
	count(*) as `上榜次数`,
	max(a.zdf) as `最大涨跌幅`,
	min(a.zdf) as `最小涨跌幅`,
	collect_set(dt) as `日期集`
from
	stock.bx_day_rise_top10 as a
where
	yearmonth = ${yearmonth}
group by
	a.code,
	a.name
sort by `上榜次数` desc;

