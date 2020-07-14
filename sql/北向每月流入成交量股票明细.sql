set hivevar:yearmonth='202006';

select
	bx_volumn.xh as `榜几`,
	bx_volumn.code as `股票代码`,
	bx_volumn.name as `股票名称`,
	bx_volumn.zdf as `涨跌幅`,
	bx_volumn.jme as `北向净买额`,
	bx_volumn.mrje as `北向买入金额`,
	bx_volumn.mcje as `北向卖出金额`,
	bx_volumn.cjje as `北向成交金额`,
	details.open as `开盘价`,
	details.high as `最高价`,
	details.low as `最低价`,
	details.close as `收盘价`,
	details.volume as `成交数量/股`,
	details.amount as `成交金额/元`,
	details.adjustflag as `复权类型`,
	details.turn as `换手率`,
	details.tradestatus as `交易状态`,
	details.pctChg as `涨跌幅`,
	details.peTTM as `滚动市盈率`,
	details.pbMRQ as `市净率`,
	details.psTTM as `滚动市销率`,
	details.pcfNcfTTM as `滚动市现率`,
	details.isST as `是否ST股`,
	bx_volumn.dt as `日期`,
	bx_volumn.weekday as `星期`
from
(
	select
		xh, code, name, spj, zdf, jme, mrje, mcje, cjje, jys, dt, dt2, weekday
	from stock.bx_day_volume_top10
	where yearmonth=${yearmonth}
)bx_volumn

left join
(
	select
		dt, substr(code, 4, 6)code, open, high, low, close,
		volume, amount, adjustflag, turn, tradestatus, pctChg,
		peTTM, pbMRQ, psTTM, pcfNcfTTM, isST,
		row_number() over(partition by substr(code, 4, 6), dt order by if(peTTM!=0, 1, 0)desc)num --去除非股票的指数
	from stock.stock_details
	where yearmonth=${yearmonth}
)details
on bx_volumn.dt2=details.dt and bx_volumn.code=details.code and num=1;