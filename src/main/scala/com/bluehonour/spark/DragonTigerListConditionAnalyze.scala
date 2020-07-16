package com.bluehonour.spark

import org.apache.spark.sql.SparkSession

object DragonTigerListConditionAnalyze {
  val YEAR_MONTH = "202006"
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
        |insert overwrite table stock.dragon_tiger_list_condition_analyze partition(yearmonth=${YEAR_MONTH})
        |select
        |	condition,
        |	funding_source,
        |	trade_type,
        |	total_time,
        |	t1_rise_time,
        |	t2_rise_time,
        |	t5_rise_time,
        |	t10_rise_time,
        |	t1_rise_time/total_time as t1_rise_frequency,
        |	t2_rise_time/total_time as t2_rise_frequency,
        |	t5_rise_time/total_time as t5_rise_frequency,
        |	t10_rise_time/total_time as t10_rise_frequency
        |from
        |(
        |	select
        |		sbyy as condition,
        |		funding_source,
        |		trade_type,
        |		count(*) as total_time,
        |		sum(if(d.zdf_t1>0, 1, 0)) as t1_rise_time,
        |		sum(if(d.zdf_t2 is not null and d.zdf_t2>d.zdf_t1, 1, 0)) as t2_rise_time,
        |		sum(if(d.zdf_t2 is not null and d.zdf_t5 is not null and d.zdf_t5>d.zdf_t2, 1, 0)) as t5_rise_time,
        |		sum(if(d.zdf_t5 is not null and d.zdf_t10 is not null and d.zdf_t10>d.zdf_t5, 1, 0)) as t10_rise_time
        |	from stock.dragon_tiger_list_aggregate_analyze d
        |	where yearmonth=${YEAR_MONTH}
        |	group by
        |		sbyy, funding_source, trade_type
        |)a
        |order by
        |	total_time desc,
        |	t1_rise_time desc,
        |	t2_rise_time desc,
        |	t5_rise_time desc,
        |	t10_rise_time desc,
        |	t1_rise_frequency desc,
        |	t2_rise_frequency desc,
        |	t5_rise_frequency desc,
        |	t10_rise_frequency desc
        |""".stripMargin).show()
  }
}