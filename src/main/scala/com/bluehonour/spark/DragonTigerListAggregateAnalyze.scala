package com.bluehonour.spark

import org.apache.spark.sql.SparkSession

object DragonTigerListAggregateAnalyze {
  val YEAR_MONTH = "202005"
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName(s"${this.getClass.getCanonicalName}")
      .master("local[4]")
//      .master("spark://master:7077")
      // 连接hive地址，如果复制hive-site.xml到resources下，则不需要此配置
      .config("hive.metastore.uris", "thrift://master:9083")
      .enableHiveSupport()
      .getOrCreate()
    val context = spark.sparkContext
    context.setLogLevel("WARN")

    spark.sql("use stock")
    spark.sql(
      s"""
        |insert overwrite table stock.dragon_tiger_list_aggregation_analysis partition(yearmonth=${YEAR_MONTH})
        |select
        |	code,
        |	name,
        |	dt,
        |	case when flag>0 then '涨'
        |		when flag=0 then '不涨不跌'
        |		when flag<0 then '跌'
        |		else ''
        |		end	as is_rise,
        |	case when trading=2 then '买'
        |		when trading=1 then '做T'
        |		when trading=0 then '卖'
        |		else ''
        |		end as trade_type,
        |	case when fund_source=2 then '主力'
        |		when fund_source=1 then '机构'
        |		when fund_source=0 then '游资'
        |		else ''
        |		end as funding_source,
        |	jd,
        |	spj,
        |	zdf,
        |	jme,
        |	mrje,
        |	mcje,
        |	cjje,
        |	sczcjje,
        |	jmje_rate,
        |	cjje_rate,
        |	hsl,
        |	ltsz,
        |	sbyy,
        |	nvl(t1, '') as zdf_t1,
        |	nvl(t2, '') as zdf_t2,
        |	nvl(t5, '') as zdf_t5,
        |	nvl(t10, '') as zdf_t10,
        |	weekday
        |from
        |(
        |	select *,
        |		case when zdf>0 then 1
        |			when zdf=0 then 0
        |			when zdf<0 then -1
        |			else -2
        |			end as flag,
        |		case when jd like '%买%' then 2
        |			when jd like '做T' then 1
        |			when jd like '%卖%' then 0
        |			else -1
        |			end as trading,
        |		case when jd like '%主力%' then 2
        |			when jd like '%机构%' then 1
        |			when jd like '%游资%' then 0
        |			else -1
        |			end as fund_source
        |	from
        |	(
        |		select code, name, dt, jd, spj, zdf, jme, mrje, mcje, cjje, sczcjje, jmje_rate, cjje_rate, hsl, ltsz, sbyy, t1, t2, t5, t10, weekday
        |		from stock.history_dragon_tiger_list
        |		where yearmonth='${YEAR_MONTH}'
        |	)list
        |	sort by
        |	flag desc,
        |	trading desc,
        |	fund_source desc,
        |	sbyy desc,
        |	zdf desc,
        |	t10 desc,
        |	t5 desc,
        |	t2 desc,
        |	t1 desc
        |)a
        |""".stripMargin).show(false)
  }
}
