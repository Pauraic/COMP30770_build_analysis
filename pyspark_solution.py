from pyspark import SparkContext,SparkConf
import json # to parse string
import time

starttime = time.time()


#at least "threshold" entries to be considered
threshold = 10
#target files/directory - wildcard format
dir = "data/*.json"

#pass more memory to spark, tweak the numbers?
conf = SparkConf().setAppName("godsbywinrate").set("spark.executor.memory", "9g").set("spark.driver.memory", "4g").set("spark.executor.memoryOverhead","1g")\
    .set("spark.driver.memoryOverhead","2g")
#context
sc = SparkContext(conf=conf)

#lazy read files, load each into separate partition
rdd = sc.textFile(dir,minPartitions=8)

#each line has trailing comma, just handling it here with the last character removal
def process_file(x):
    return (json.loads(line[:-1]) for line in x.splitlines() if line.strip() != "" and isjson(line[:-1]))

#clean out malformed lines - maybe there is a better way to do this?
def isjson(x):
    try:
        json.loads(x)
        return True
    except ValueError:
        return False

#json.loads to take the json format string and cut it up
duels = rdd.flatMap(lambda x: process_file(x)).filter(lambda r :  r.get("match_queue_id",-1) == 440 )

#just keep 2 columns
clean = duels.map(lambda x: (x.get("Reference_Name","Unknown"),1 if x.get("Win_Status") == "Winner" else 0))

#effivient alternative to grouping
agg = clean.combineByKey(
    lambda v: (v,1),                    #tracks the counter
    lambda a,v:(a[0]+v,a[1]+1),         #value,count
    lambda a1,a2: (a1[0]+a2[0],a1[1]+a2[1]) #add 2 together
).filter(lambda x: x[1][1] >= threshold).mapValues(lambda a : a[0]/a[1] if a[1]>0 else 0)
##map takes the tuple and unfolds it

sorted = agg.sortBy( lambda x: x[1], ascending=False)
print(sorted.collect())
print("finish time: ",time.time()-starttime)
