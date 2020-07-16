--bx_history_volume
load data local inpath '/home/xxx/stock-data/bx_history_volume/20200701-20200706' overwrite into table stock.bx_day_volume_top10 partition(yearmonth=${yearmonth});
--history_dragon_tiger_list
load data local inpath '/home/xxx/stock-data/history_dragon_tiger_list/20200701-20200710' overwrite into table stock.history_dragon_tiger_list partition(yearmonth=${yearmonth});
--dragon_tiger_list
load data local inpath '/home/xxx/stock-data/dragon_tiger_list/202007' overwrite into table stock.dragon_tiger_list partition(yearmonth=${yearmonth});
--bx_day_rise_top10
load data local inpath '/home/xxx/stock-data/bx_day_rise_top10/202007' overwrite into table stock.bx_day_rise_top10 partition(yearmonth=${yearmonth});
--sector_fund_flow
load data local inpath '/home/xxx/stock-data/sector_fund_flow/202007' overwrite into table stock.sector_fund_flow partition(yearmonth=${yearmonth});
--bx_day_volume_top10
load data local inpath '/home/xxx/stock-data/bx_day_volume_top10/202007' overwrite into table stock.bx_day_volume_top10 partition(yearmonth=${yearmonth});
--bx_history_date
load data local inpath '/home/xxx/stock-data/bx_history_date/20200601-20200630' into table stock.bx_action_date;
--all_stock_data_details
load data local inpath '/home/xxx/stock-data/all_stock_data_details/2020-03' into table stock.stock_details partition(yearmonth=${yearmonth});
