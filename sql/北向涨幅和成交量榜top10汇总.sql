insert overwrite table stock.top10 partition(yearmonth=${yearmonth})
select
	bx.code as code,
	name,
	time,
	max_zdf,
	min_zdf,
	(last_price-first_price)/first_price*100 as month_zdf,
	classify,
	date_set
from
(
	select
		code,
		max(name) as name,
		count(*) as time,
		max(zdf) as max_zdf,
		min(zdf) as min_zdf,
		classify,
		collect_set(dt) as date_set
	from
	(
		select code, name, dt, zdf, '涨幅' as classify
		from stock.bx_day_rise_top10
		where yearmonth=${yearmonth}
		UNION
		select code, name, dt, zdf, '成交量' as classify
		from stock.bx_day_volumn_top10
		where yearmonth=${yearmonth}
	)tmp
	group by code, classify
)bx
left join
(
	select code,
		first_value(close) over(partition by code order by dt asc)first_price,
		first_value(close) over(partition by code order by dt desc)last_price,
		row_number() over(partition by code order by dt asc)num
	from
	(
		select substr(code, 4, 6)code, close, dt,
			row_number() over(partition by substr(code, 4, 6), dt order by if(peTTM!=0, 1, 0)desc)num --去除非股票的指数
		from stock.stock_details
		where yearmonth=${yearmonth}
	)tmp
	where tmp.num=1
)details
on bx.code=details.code and details.num=1

sort by
	time desc,
	month_zdf desc