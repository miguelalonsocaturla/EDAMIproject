
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import json


def listweets():
    df = pd.read_csv('covidvaccine.csv', usecols=['text'])
    df.info(verbose=False, memory_usage="deep")
    list1 = df.values.tolist()

    hashtag1 = []
    num = 10000
    for i in range(num):
        hashtag1.append(re.findall(r"#(\w+)", json.dumps(list1[i])))
    list3 = [x for x in hashtag1 if x != []]
    print(len(list3))
    return list3
