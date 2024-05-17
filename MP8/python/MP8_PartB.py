from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

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
# 2. Counting : How many lines does the file contains? Answer this question via both RDD api & #Spark SQL
####

# Spark SQL
gb_df.createOrReplaceTempView("gbooks")

query = "SELECT COUNT(*) FROM gbooks"
results = spark.sql(query)
results.show()

# sqlContext.sql(query).show() or df.show()
# +--------+
# |count(1)|
# +--------+
# |   50013|
# +--------+



