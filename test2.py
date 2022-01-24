

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import json


def listtweets():
    df = pd.read_csv('database/covidvaccine.csv', usecols=['text'])
    df.info(verbose=False, memory_usage="deep")
    list = df.values.tolist()

    hashtags = []
    for i in range(len(list)//50):

        hashtags.append(re.findall(r'\B#\w*[a-zA-Z]+\w*', json.dumps(list[i])))
    list3 = [x for x in hashtags if x is not []]
    print(len(list3))
    return list3
