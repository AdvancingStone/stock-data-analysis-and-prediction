set hivevar:yearmonth='202006';
--北向每月流入成交量榜单汇总
select
	code as `股票代码`,
	name as `股票名称`,
	count(*) as `上榜次数`,
	collect_set(dt) as `日期集`
from
	stock.bx_day_volume_top10 as a
where
	yearmonth = ${yearmonth}
group by
	a.code,
	a.name
sort by `上榜次数` desc;