from pyspark import SparkContext,SparkConf
import json # to parse string

conf = SparkConf().setAppName("godsbywinrate").set("spark.executor.memory", "8g").set("spark.driver.memory", "4g").set("spark.executor.memoryOverhead","1g")
sc = SparkContext(conf=conf)

file = "match_details_2024-02-20.json"
#file = "test.json"

#print(rdd.take(1))
with open (file,'r') as f:
    duels = sc.parallelize(json.load(f))#.filter(lambda r: r["match_queue_id"] == 440)

clean = duels.map(lambda x: (x["Reference_Name"],1 if x["Win_Status"] == "Winner" else 0))
#print(clean.collect())
agg = clean.combineByKey(
    lambda v: (v,1),                    #tracks the counter
    lambda a,v:(a[0]+v,a[1]+1),         #value,count
    lambda a1,a2: (a1[0]+a2[0],a1[1]+a2[1]) #add 2 together
                   ).mapValues(lambda a : a[0]/a[1] if a[1]>0 else 0)
##map takes the tuple and unfolds it
print(agg.collect())
