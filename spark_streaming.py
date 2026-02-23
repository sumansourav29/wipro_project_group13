from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EnergyStreaming") \
    .getOrCreate()

schema = """
Department STRING,
Electricity Usage FLOAT
"""

stream_df = spark.readStream \
    .format("csv") \
    .option("header", True) \
    .schema(schema) \
    .load("data/stream/")

query = stream_df.groupBy("Department") \
    .sum("Electricity Usage") \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
