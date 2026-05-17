from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FinSightSpark") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

# Read from Postgres
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/finsight") \
    .option("dbtable", "transactions") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .load()

# DAILY REVENUE AGGREGATION
daily = df.groupBy("currency").sum("amount", "fee", "net")

# Write back to Postgres
daily.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/finsight") \
    .option("dbtable", "daily_revenue_agg") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .mode("overwrite") \
    .save()