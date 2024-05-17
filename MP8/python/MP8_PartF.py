from pyspark.sql.functions import col, lag, lead, when,count, sum as spark_sum
from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()

####
# 1. Setup : Write a function to load it in an RDD & DataFrame
####

# RDD API
# Columns:
# 0: word (string), 1: year (int), 2: frequency (int), 3: books (int)
gbook = sc.textFile("gbooks")
gbook = gbook.map(lambda s:s.split()).map(lambda line:[line[0], int(line[1]), int(line[2]), int(line[3])])
fields = [StructField('word', StringType(), True),
          StructField('year', IntegerType(), True),
          StructField('frequency', IntegerType(), True),
          StructField('books', IntegerType(), True)]
schema = StructType(fields)
gb_df = spark.createDataFrame(gbook, schema)

gbook_filtered = gb_df.filter((col("year") >= 1500) & (col("year") <= 2000))
window_spec = Window.partitionBy("word").orderBy("year")
# gbook_freq_increase = gbook_filtered.withColumn("frequency_increase", col("frequency") + lag("frequency", 1).over(window_spec))
# total_freq_increase = gbook_freq_increase.groupBy("word").agg(spark_sum("frequency_increase").alias("total_increase"))
# result = total_freq_increase.select("word", "total_increase").orderBy("total_increase", ascending=False)
# result.show()

gbook_freq_increase = gbook_filtered.withColumn("frequency_increase",coalesce(lag(col("frequency"), -1).over(window_spec),lit(0)))
total_freq_increase = gbook_freq_increase.groupBy("word").agg(spark_sum("frequency_increase").alias("total_increase"))
result = total_freq_increase.select("word", "total_increase").orderBy("total_increase", ascending=False)
result.show()