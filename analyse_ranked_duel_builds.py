#prototyping against 1 file

#analysis question: winrate by god in ranked duel

# parameters/query info:
#god name : Reference_Name
#match_queue_id = 440  (ranked duel)
#Win_Status : "Winner" / "Loser" - group and take avg

import pandas as pd
import json


result_by_god = []

with open('match_details_2024-02-20.json','r') as f:

    i = 0
    data = json.load(f)
    for record in data:
        if record["match_queue_id"] == 440:
            godname = record["Reference_Name"]
            result = 1 if record["Win_Status"] == 'Winner' else  0
            result_by_god.append({"god":godname,"winrate":result})
            i = i+1 
            if i > 100:
                break

    tempdf = pd.DataFrame(result_by_god)
    df = tempdf.groupby("god",as_index=False)["winrate"].mean()

    print(df)

