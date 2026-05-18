from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, sum, avg

def currency_aggregations(df: DataFrame):
    return df.groupBy("currency").agg(
        count("*").alias("txn_count"),
        sum("amount").alias("total_amount"),
        sum("net").alias("total_net"),
        avg("amount").alias("avg_amount")
    )


def status_aggregations(df: DataFrame):
    return df.groupBy("payment_status").agg(
        count("*").alias("count"),
        sum("amount").alias("total_amount")
    )


def category_aggregations(df: DataFrame):
    return df.groupBy("reporting_category").agg(
        count("*").alias("count"),
        sum("amount").alias("total_amount")
    )