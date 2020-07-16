insert overwrite table stock.dragon_tiger_list_condition
select '连续三个交易日内，涨幅偏离值累计达到20的证券' as condition
union select '连续三个交易日内，涨幅偏离值累计达到12的ST证券、*ST证券' as condition
union select '连续三个交易日内，涨幅偏离值累计达到12的ST证券、*ST证券和未完成股改证券' as condition
union select '连续三个交易日内，日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20的证券' as condition
union select '连续三个交易日内，跌幅偏离值累计达到20的证券' as condition
union select '连续三个交易日内,跌幅偏离值累计达到12的ST证券、*ST证券' as condition
union select '连续三个交易日内，跌幅偏离值累计达到12的ST证券、*ST证券和未完成股改证券' as condition
union select '非ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到20的证券' as condition
union select '日换手率达到20的前五只证券' as condition
union select '有价格涨跌幅限制的日价格振幅达到15的前三只证券' as condition
union select '日振幅值达到15的前五只证券' as condition
union select '有价格涨跌幅限制的日收盘价格涨幅偏离值达到7的前三只证券' as condition
union select '有价格涨跌幅限制的日收盘价格涨幅达到15的前五只证券' as condition
union select '有价格涨跌幅限制的日换手率达到30的前五只证券' as condition
union select '无价格涨跌幅限制的证券' as condition
union select '退市整理的证券' as condition
union select '退市整理期' as condition
union select '当日无价格涨跌幅限制的A股，出现异常波动停牌的' as condition
union select '日跌幅偏离值达到7的前五只证券' as condition
union select 'ST、*ST和S证券连续三个交易日内收盘价格跌幅偏离值累计达到15的证券' as condition