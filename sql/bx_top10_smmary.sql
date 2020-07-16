set hivevar:yearmonth='202006';

--北向涨幅和成交量榜top10汇总
insert overwrite table stock.bx_top10_smmary partition(yearmonth=${yearmonth})
select
	bx.code as code,
	name,
	nvl(last_month.history_jme, 0)+month_jme as history_jme,
	month_jme,
	time,
	max_zdf,
	min_zdf,
	(last_price-first_price)/first_price*100 as month_zdf, --该结果仅供参考，因为stock details采用不复权，可能导致结果差异很大
	bx.classify as classify,
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
		sum(jme) as month_jme,
		collect_set(dt) as date_set
	from
	(
		select code, name, dt, zdf, '涨幅' as classify, '' as jme
		from stock.bx_day_rise_top10
		where yearmonth=${yearmonth}

		union

		select code, name, dt, zdf, classify,
			case when jme like '%万%' then substr(jme, 0, length(jme)-1)*10000
				when jme like '%亿%' then substr(jme, 0, length(jme)-1)*100000000
				else ''
				end as jme
		from
		(
			select code, name, dt, zdf, '成交量' as classify, jme
			from stock.bx_day_volumnbx_day_volume_top10_top10
			where yearmonth=${yearmonth}
		)volume
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

left join
(
	select code, history_jme, classify,
	    row_number() over(partition by code, classify)num
	from stock.bx_top10_smmary
	where yearmonth=substr(from_unixtime(unix_timestamp('${yearmonth}01', 'yyyyMMdd')-86400, 'yyyyMMdd'), 0, 6)
)last_month
on bx.code=last_month.code and bx.classify=last_month.classify and last_month.num=1

sort by
	time desc,
	month_zdf desc