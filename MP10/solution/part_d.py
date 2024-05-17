from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint

sc = SparkContext()

RF_NUM_TREES = 80
RF_MAX_DEPTH = 30
RF_MAX_BINS = 32
RANDOM_SEED = 0

def predict(training_data, test_data):
    # TODO: Train random forest classifier from given data
    # Result should be an RDD with the prediction of the random forest for each
    # test data point
    model = RandomForest.trainClassifier(training_data, numClasses=2, categoricalFeaturesInfo={},
                                         numTrees=RF_NUM_TREES, featureSubsetStrategy="auto", impurity="gini",
                                         maxDepth=RF_MAX_DEPTH, maxBins=RF_MAX_BINS, seed=RANDOM_SEED)
    return model.predict(test_data)


if __name__ == "__main__":
    raw_training_data = sc.textFile("dataset/training.data")
    raw_test_data = sc.textFile("dataset/test-features.data")

    # TODO: Parse RDD from raw training data
    # Hint: Look at the format of data required by the random forest classifier
    # Hint 2: map() can be used to process each line in raw_training_data and
    # raw_test_data
    training_data = raw_training_data.map(lambda line: [float(x) for x in line.split(',')])
    training_data = training_data.map(lambda row: LabeledPoint(row[-1], row[0:-1]))

    # TODO: Parse RDD from raw test data
    # Hint: Look at the data format required by the random forest classifier
    test_data = raw_test_data.map(lambda line: [float(x) for x in line.split(',')])

    predictions = predict(training_data, test_data)

    # You can take a look at dataset/test-labels.data to see if your
    # predictions were right
    for pred in predictions.collect():
        print(int(pred))