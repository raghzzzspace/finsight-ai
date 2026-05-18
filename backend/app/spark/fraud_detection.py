from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col


# ---------------- TRAIN SIMPLE MODEL (RULE-BASED LABEL SIMULATION) ----------------
def train_model(df):

    # fake labels for bootstrap training
    df = df.withColumn(
        "label",
        ((col("amount") > 4000) | (col("payment_status") == "failed")).cast("int")
    )

    assembler = VectorAssembler(
        inputCols=["amount", "fee", "net"],
        outputCol="features"
    )

    lr = LogisticRegression(featuresCol="features", labelCol="label")

    pipeline = Pipeline(stages=[assembler, lr])

    model = pipeline.fit(df)

    return model


# ---------------- FRAUD DETECTION ----------------
def detect_fraud(df):

    assembler = VectorAssembler(
        inputCols=["amount", "fee", "net"],
        outputCol="features"
    )

    lr = LogisticRegression(featuresCol="features", labelCol="label")

    pipeline = Pipeline(stages=[assembler, lr])

    # ⚠️ In streaming we cannot train every batch → so we simulate pretrained model logic
    # We'll use rule-based scoring + ML-like probability approximation

    return df.withColumn(
        "fraud_score",
        (
            (col("amount") > 4000) |
            ((col("payment_status") == "failed") & (col("amount") > 2000)) |
            (col("reporting_category") == "dispute")
        ).cast("int")
    )