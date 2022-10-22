from csv import writer
import json 
from typing import Set, Tuple
import pandas as pd
from py2neo import Graph

# #Connection to neo4j db
# SERVER_ADRESSE = "bolt://localhost:7687"
# SERVER_AUTH = ("neo4j", "bioinfo")
# graph = Graph(SERVER_ADRESSE, auth=SERVER_AUTH)

# q = "match (u:User) return u.name as username" #Database requete
# res = graph.run(q).to_table()
# for record in res :
#     print(record[0])

#CONST.

IN_CATEGORY = "IN_CATEGORY"
IN_CITY = "IN_CITY"
IN_AREA = "IN_AREA"


#import location for json files
data_folder = r"./data"
restaurants_json_file = data_folder + "/yelp_restaurants.json"
review_json_file = data_folder + "/yelp_review.json"
user_json_file = data_folder + "/yelp_user.json"

files_list = [restaurants_json_file, review_json_file, user_json_file]

#csv files for import
resto_nodes_csv = pd.DataFrame
user_nodes_csv = pd.DataFrame

# restaurants_nodes_csv = "restaurants.csv"
# review__nodes_csv = "review.csv"
# user_nodes_csv = "user.csv"
# city_nodes_csv = "city.csv"
# area_nodes_csv = "area.csv"
# ambiance_nodes_csv = "ambiance.csv"
# price_nodes_csv = "price.csv"

#relation file
friends_relationship_csv_file = "friends_relationship_csv"

# nodes_files = [restaurants_nodes_csv, review__nodes_csv, user_nodes_csv, city_nodes_csv, area_nodes_csv, ambiance_nodes_csv, price_nodes_csv]

#write user csv file 
friends_relationship_fieldname = [":START_ID(user)",":END_ID(user)"]
friends_relationship_csv = pd.DataFrame(friends_relationship_csv_file)
friends_relation_writer = friends_relationship_csv.to_csv("friens_relationship.csv", index=False, header=friends_relationship_fieldname, quotechar='"')

def write_user_nodes():
    user_json = json.loads(open(user_json_file).read())
    fieldnames = ["user_id:ID(user)","name", "review_count","yelping_since"]
    user_nodes_csv.to_csv(header=fieldnames, quotechar='"')  
    for line in user_json:
        line = line.strip()
        json_node = json.load(line)
           


    
# csv file 
write_user_nodes()

#friends_relationship_csv = open(friends_relationship_csv_file, mode="w", newline="\n")


exit()

with open(file) as data_file:
    json = json.load(data_file)

pdObj = pd.read_json('export.json', orient='index')
print(pdObj)
csvData = pdObj.to_csv(index=False)
print(csvData)

pdObj.to_csv('streaming.csv', index=False)
