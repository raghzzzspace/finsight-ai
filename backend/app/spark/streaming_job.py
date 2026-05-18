from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

from app.spark.aggregations import (
    currency_aggregations,
    status_aggregations,
    category_aggregations
)

from app.spark.fraud_detection import detect_fraud
from app.spark.postgres_writer import write_to_postgres_batch

# ---------------- SPARK SESSION ----------------
spark = SparkSession.builder \
    .appName("FinSightStreaming") \
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8"
    ) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


# ---------------- KAFKA SOURCE ----------------
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions-events") \
    .option("startingOffsets", "latest") \
    .load()


# ---------------- SCHEMA ----------------
schema = StructType([
    StructField("event_id", StringType()),
    StructField("transaction_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("merchant_id", StringType()),
    StructField("amount", FloatType()),
    StructField("fee", FloatType()),
    StructField("net", FloatType()),
    StructField("currency", StringType()),
    StructField("payment_status", StringType()),
    StructField("reporting_category", StringType()),
    StructField("created_at", StringType()),
])


# ---------------- PARSE JSON ----------------
json_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")


# ---------------- FRAUD DETECTION (ML) ----------------
fraud_df = detect_fraud(json_df)


# ---------------- AGGREGATIONS ----------------
currency_df = currency_aggregations(json_df)
status_df = status_aggregations(json_df)
category_df = category_aggregations(json_df)


# ---------------- STREAMS ----------------
query1 = currency_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query2 = status_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query3 = category_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()


# ---------------- FRAUD ALERT STREAM ----------------
fraud_query = fraud_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# ---------------- POSTGRES WRITER ----------------
def foreach_batch_function(df, epoch_id):
    print(f"[POSTGRES] Batch {epoch_id} received {df.count()} rows")
    write_to_postgres_batch(df)

query_pg = fraud_df.writeStream \
    .outputMode("append") \
    .foreachBatch(foreach_batch_function) \
    .start()

# ---------------- KEEP ALIVE ----------------
query1.awaitTermination()
query2.awaitTermination()
query3.awaitTermination()
fraud_query.awaitTermination()
query_pg.awaitTermination()