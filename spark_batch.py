from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EnergyBatchProcessing") \
    .getOrCreate()

df = spark.read.csv(
    "data/energy_consumption.csv",
    header=True,
    inferSchema=True
)

df.groupBy("Department") \
  .sum("Electricity Usage") \
  .show()

spark.stop()
