from pyspark import *
from numpy import array
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.sql.types import *

############################################
#### PLEASE USE THE GIVEN PARAMETERS     ###
#### FOR TRAINING YOUR KMEANS CLUSTERING ###
#### MODEL                               ###
############################################

NUM_CLUSTERS = 4
SEED = 0
MAX_ITERATIONS = 100
INITIALIZATION_MODE = "random"

sc = SparkContext()

spark = SparkSession.builder.appName('fun').getOrCreate()


def get_clusters(data_rdd, num_clusters=NUM_CLUSTERS, max_iterations=MAX_ITERATIONS,
                 initialization_mode=INITIALIZATION_MODE, seed=SEED):
    # TODO:
    # Use the given data and the cluster pparameters to train a K-Means model
    # Find the cluster id corresponding to data point (a car)
    # Return a list of lists of the titles which belong to the same cluster
    # For example, if the output is [["Mercedes", "Audi"], ["Honda", "Hyundai"]]
    # Then "Mercedes" and "Audi" should have the same cluster id, and "Honda" and
    # "Hyundai" should have the same cluster id
    result = []
    clusters = KMeans.train(data_rdd, num_clusters, maxIterations=max_iterations,
                            initializationMode=initialization_mode, seed=seed)

    ids = f.map(lambda line: (clusters.predict(line.strip().split(",")[1:]), line.strip().split(",")[0]))
    ids = ids.groupByKey().map(lambda x: (x[0], list(x[1])))
    [result.append(line[1]) for line in ids.collect()]
    # https://stackoverflow.com/questions/29717257/pyspark-groupbykey-returning-pyspark-resultiterable-resultiterable
    return result


if __name__ == "__main__":
    f = sc.textFile("dataset/cars.data")
    data_rdd = f.map(lambda line: [float(x) for x in line.strip().split(",")[1:]])

    # TODO: Parse data from file into an RDD

    clusters = get_clusters(data_rdd)

    for cluster in clusters:
        print(','.join(cluster))