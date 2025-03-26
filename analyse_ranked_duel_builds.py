#prototyping against 1 file

#analysis question: winrate by god in ranked duel

# parameters/query info:
#god name : Reference_Name
#match_queue_id = 440  (ranked duel)
#Win_Status : "Winner" / "Loser" - group and take avg

import pandas as pd
import json
import time

threshold = 10 # number of dataset games of specific god
files = ["match_details_2024-02-20.json",
         "match_details_2024-02-21.json",
         "match_details_2024-02-22.json",
         "match_details_2024-02-23.json",
         "match_details_2024-02-24.json"]#,"match_details_2024-02-25.json"]

starttime = time.time()
result_by_god = []


for name in files:
    filepath = f"data/{name}"
    print("working on file: ",filepath)
    with open(filepath,'r') as f:

        data = json.load(f)
        for record in data:
            if record["match_queue_id"] == 440:
                godname = record["Reference_Name"]
                result = 1 if record["Win_Status"] == 'Winner' else  0
                result_by_god.append({"god":godname,"winrate":result})

tempdf = pd.DataFrame(result_by_god)
print("loading time : ", time.time()-starttime)
print(f"{len(tempdf)} <- length of df")

starttime = time.time()
filtered = tempdf.groupby("god").filter(lambda x: len(x) >= threshold)
df = filtered.groupby("god",as_index=False)["winrate"].mean().sort_values(by="winrate",ascending=False)

print("filtering and grouping data time: ",time.time()-starttime)
print(df)

