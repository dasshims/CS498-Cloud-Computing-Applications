#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 

#TODO
def link_count_mapper(line):
    page_id, targets = line.strip().split(': ')
    targets = targets.strip().split(' ')
    targets = [t.strip() for t in targets]
    targets = filter(lambda x: len(x) > 0, targets)

    to_return = [(t, 1) for t in targets]
    return to_return

counts = lines.flatMap(link_count_mapper).reduceByKey(lambda a, b: a + b)

counts = counts.sortByKey(ascending=False)

tops = counts.sortBy(ascending=False, keyfunc=lambda a: a[1]).take(10)
top_10_pages = sorted(tops)

#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")
output = open(sys.argv[2], "w")
for page, count in top_10_pages:
    output.write(f"{page}\t{count}\n")

output.close()

sc.stop()

