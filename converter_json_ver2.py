import pandas as pd
import json
import csv

# json files
# data_folder = r"./data"
# user_json_file = data_folder + "/yelp_user.json"

# data = json.loads(open(user_json_file).read())
# data2 = pd.json_normalize(data)
# data3 = pd.DataFrame(data2)
# data3.to_csv("output.csv", index = False, sep=',', header=TRUE)

# csv nodes 

# user_nodes_csv = pd.DataFrame

# csv relationship 

# friendship_relationship_csv = pd.DataFrame


# conversion

user_json = json.loads(open("data/yelp_user.json").read())
print(type(user_json))

exit()

with open("data2/yelp_user.json", "r") as json:
    user_json = json.loads(json)
    print(json)
    exit()

    normalize = pd.json_normalize(user_json)
    print(normalize)
    exit()




# df = pd.read_json(user_json_file, typ='frame',orient='records')

df = pd.DataFrame(normalize)
user_csv = df.to_csv("user.csv",index=False, sep=",", quotechar='"')

f = open("data\yelp_user.json")
data = pd.read_json(f)

# print(data)
# print(pd.json_normalize(data))
print(data.to_string())
data.to_csv("output.csv", index=False, header=True)

# print(pd.json_normalize(json_list))
# print(pd.json_normalize(f))
