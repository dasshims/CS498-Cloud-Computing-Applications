import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
# Get Spark context
sc = SparkContext()
# From spark context get glue context and spark session
glueContext = GlueContext(sc)
# Create and init job
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Begin TODOs - add your code starting from here. Comments
# are provided for each statement that you may need to add.

# 1. Create a Glue client to access the Data Catalog API
glue_client = boto3.client('glue')

# 2. Create a dynamic frame from AWS Glue catalog table.
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(database="cs498-mp9", table_name="flights_after_job_1")

# 3. Get Spark dataframe from the Glue dynamic frame created above
spark_df = dynamic_frame.toDF()

# 4. Create a new time_zone_difference column and add it to the Spark data frame.
spark_df = spark_df.withColumn("time_zone_difference",
                               ((col("scheduled_arrival") / 100) * 60 + (col("scheduled_arrival") % 100)) -
                               (((col("scheduled_departure") / 100) * 60 + (col("scheduled_departure") % 100) + col("scheduled_time")) % (24 * 60)
                              ))

# 5. Convert Spark data frame back to Glue dynamic frame
dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, "dynamic_frame")

# 6. Get the existing Glue catalog table schema.
table_info = glue_client.get_table(DatabaseName="cs498-mp9", Name="flights_after_job_1")

# 7. Delete unnecessary fields from the table schema
fields_to_delete = ['UpdateTime', 'IsRegisteredWithLakeFormation', 'CreatedBy', 'DatabaseName', 'CreateTime', 'CatalogId', 'VersionId']
for field in fields_to_delete:
    if field in table_info['Table']:
        del table_info['Table'][field]

# 8. Define the new column 'time_zone_difference' to be added to the table schema
new_column = {
    "Name": "time_zone_difference",
    "Type": "int"
}

# 9. Append the new column info to the table dictionary columns list
table_info['Table']['StorageDescriptor']['Columns'].append(new_column)

# 10. Update the table with the new schema.
glue_client.update_table(DatabaseName="cs498-mp9", TableInput=table_info['Table'])

# 11. Get the output S3 bucket
output_bucket = glueContext.getSink(connection_type="s3", path="s3://cs498-mp9/")

# 12. Set the catalog database and table
output_bucket.setCatalogInfo(database="cs498-mp9", tableName="flights_after_job_2")

# 13. Set the format to 'json'
output_bucket.setFormat("json")

# 14. Write data into S3 bucket
output_bucket.writeFrame(dynamic_frame)

# End TODOs

# Commit job
job.commit()
