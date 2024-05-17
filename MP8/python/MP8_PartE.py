from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()
####
# 1. Setup : Write a function to load it in an RDD & DataFrame
####

# RDD API
# Columns:
# 0: word (string), 1: year (int), 2: frequency (int), 3: books (int)


# Spark SQL - DataFrame API
gbook = sc.textFile("gbooks")
gbook = gbook.map(lambda s:s.split()).map(lambda line:[line[0], int(line[1]), int(line[2]), int(line[3])])
fields = [StructField('word', StringType(), True),
          StructField('year', IntegerType(), True),
          StructField('frequency', IntegerType(), True),
          StructField('books', IntegerType(), True)]
schema = StructType(fields)
gb_df = spark.createDataFrame(gbook, schema)

####
# 5. Joining : The following program construct a new dataframe out of 'df' with a much smaller size.
####

df2 = gb_df.select("word", "year").distinct().limit(100)
df2.createOrReplaceTempView('gbooks2') # Register table name for SQL

# Now we are going to perform a JOIN operation on 'df2'. Do a self-join on 'df2' in lines with the same #'count1' values and see how many lines this JOIN could produce. Answer this question via Spark SQL API

# Spark SQL API
results = spark.sql("SELECT a.word AS word1, b.word AS word2 FROM gbooks2 a, gbooks2 b WHERE a.year = b.year")
print(results.count())
# output: 166

