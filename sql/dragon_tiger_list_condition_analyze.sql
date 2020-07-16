set hivevar:yearmonth='202006';
--龙虎榜上榜条件分析
insert overwrite table stock.dragon_tiger_list_condition_analyze partition(yearmonth=${yearmonth})
select
	condition,
	funding_source,
	trade_type,
	total_time,
	t1_rise_time,
	t2_rise_time,
	t5_rise_time,
	t10_rise_time,
	t1_rise_time/total_time as t1_rise_frequency,
	t2_rise_time/total_time as t2_rise_frequency,
	t5_rise_time/total_time as t5_rise_frequency,
	t10_rise_time/total_time as t10_rise_frequency
from
(
	select
		sbyy as condition,
		funding_source,
		trade_type,
		count(*) as total_time,
		sum(if(d.zdf_t1>0, 1, 0)) as t1_rise_time,
		sum(if(d.zdf_t2 is not null and d.zdf_t2>d.zdf_t1, 1, 0)) as t2_rise_time,
		sum(if(d.zdf_t2 is not null and d.zdf_t5 is not null and d.zdf_t5>d.zdf_t2, 1, 0)) as t5_rise_time,
		sum(if(d.zdf_t5 is not null and d.zdf_t10 is not null and d.zdf_t10>d.zdf_t5, 1, 0)) as t10_rise_time
	from stock.dragon_tiger_list_aggregate_analyze d
	where yearmonth=${yearmonth}
	group by
		sbyy, funding_source, trade_type
)a
order by
	total_time desc,
	t1_rise_time desc,
	t2_rise_time desc,
	t5_rise_time desc,
	t10_rise_time desc,
	t1_rise_frequency desc,
	t2_rise_frequency desc,
	t5_rise_frequency desc,
	t10_rise_frequency desc