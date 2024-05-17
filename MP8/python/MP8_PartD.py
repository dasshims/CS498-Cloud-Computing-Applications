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
# 4. MapReduce : List the top three words that have appeared in the greatest number of years.
####

# Spark SQL

gb_df.createOrReplaceTempView("gbooks")
results = spark.sql("SELECT word, COUNT(*) FROM gbooks GROUP BY word ORDER BY COUNT(*) DESC")
results.show(3)

# +-------------+--------+
# |         word|count(1)|
# +-------------+--------+
# |    ATTRIBUTE|      11|
# |approximation|       4|
# |    agast_ADV|       4|
# +-------------+--------+
# only showing top 3 rows

# The above output may look slightly different for you due to ties with other words
