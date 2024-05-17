#!/usr/bin/env python

'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
from pyspark import SparkConf, SparkContext
import re

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

with open(stopWordsPath) as f:
	#TODO
	stopWords = set(f.read().strip().split('\n'))

stopWords.add('')
with open(delimitersPath) as f:
    #TODO
    delimiters = f.read().strip()

pattern = "|".join(map(re.escape, delimiters))

conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[3], 1)

#TODO
tokens = lines.flatMap(lambda line: re.split(pattern, line.lower())).map(lambda word: word.lower()).filter(lambda word: word not in stopWords)

wordCounts = tokens.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)
sortedWordCounts = wordCounts.sortBy(lambda x: x[1], ascending=False)
topWords = sortedWordCounts.take(10)

sortByWord = sorted(topWords, key=lambda x: x[0])

outputFile = open(sys.argv[4],"w")
for word, count in sortByWord:
    outputFile.write(f"{word}\t{count}\n")

outputFile.close()
sc.stop()
