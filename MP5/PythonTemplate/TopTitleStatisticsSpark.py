#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

#TODO
counts = lines.map(lambda line: int(line.split("\t")[1].strip()))

count_list = counts.collect()
num_counts = len(count_list)
total_sum = sum(count_list)
minimum = min(count_list)
maximum = max(count_list)
mean = total_sum // num_counts
variance = sum((x - mean) ** 2 for x in count_list) // num_counts


outputFile = open(sys.argv[2], "w")
'''
TODO write your output here
write results to output file. Format
outputFile.write('Mean\t%s\n' % ans1)
outputFile.write('Sum\t%s\n' % ans2)
outputFile.write('Min\t%s\n' % ans3)
outputFile.write('Max\t%s\n' % ans4)
outputFile.write('Var\t%s\n' % ans5)
'''
outputFile = open(sys.argv[2], "w")
outputFile.write('Mean\t%s\n' % mean)
outputFile.write('Sum\t%s\n' % total_sum)
outputFile.write('Min\t%s\n' % minimum)
outputFile.write('Max\t%s\n' % maximum)
outputFile.write('Var\t%s\n' % variance)

outputFile.close()
sc.stop()

