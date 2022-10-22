import json
import csv
import pandas as pd

new_dict  = [ 
  {
        "user_id": "XLs_PhrJ7Qwn_RfgMM7Djw",
        "name": "Weili",
        "review_count": 90,
        "yelping_since": "2009-07-12 14:34:54",
        "useful": 71,
        "funny": 21,
        "cool": 19,
        "elite": "",
        "friends": [],
        "fans": 1,
        "average_stars": 3.62,
        "compliment_hot": 0,
        "compliment_more": 0,
        "compliment_profile": 0,
        "compliment_cute": 0,
        "compliment_list": 0,
        "compliment_note": 1,
        "compliment_plain": 3,
        "compliment_cool": 0,
        "compliment_funny": 0,
        "compliment_writer": 0,
        "compliment_photos": 0
    },
    {
        "user_id": "IpLRJY4CP3fXtlEd8Y4GFQ",
        "name": "Robyn",
        "review_count": 518,
        "yelping_since": "2009-04-11 14:35:46",
        "useful": 1325,
        "funny": 450,
        "cool": 348,
        "elite": "2009,2010,2011",
        "friends": [
            "y3Wtx1pOvTiqsJRkjceXiw",
            "_BcWyKQL16ndpBdggh2kNA",
            "lRRuTimITgwzoXLIM3g9qw",
            "z02XKjGqJMONH59_lUHlTQ",
            "47K1MpOBhigOvjuBcDbm7Q",
            "2-RlTk9dJNpj85MR2B46Cg",
            "_hPjqzQDiyw1-4U_IAETpg",
            "dhLizr4a2oydrv15y56r0A",
            "rkxGrjk2WeAT5ZMfChT3kw",
            "pbCb0Tz0KQ0kkgaxzhWhoA",
            "Ed0GuUa_1UjbSk8qaQsHlA",
            "_LNCGYNoGKxyVUag3EG0-g",
            "B9iPTih0dmpZn6fRyZnLLg",
            "gTrKXmAx1ytdvh1xutIlfA",
            "u1gUbwyeBe8mtV97hZyImg",
            "UiRx8jyS6H957ItwFsP2nQ",
            "IPxJLWpKptzpTWlfjFiuHA",
            "srETv2HpH9fQ-7wCvCAQng",
            "cUB2WhICFuSe7DwXAIoo0g",
            "vU9_lZqJQIR8btUYw7fqxA",
            "pLZIZXIebqEcrX7IVKoJRg",
            "IWxNILja-WvurTuJWJ4skA",
            "63hpZgj7peTKizDs4zeKZA"
        ],
        "fans": 35,
        "average_stars": 2.95,
        "compliment_hot": 32,
        "compliment_more": 4,
        "compliment_profile": 2,
        "compliment_cute": 7,
        "compliment_list": 1,
        "compliment_note": 35,
        "compliment_plain": 17,
        "compliment_cool": 20,
        "compliment_funny": 20,
        "compliment_writer": 20,
        "compliment_photos": 6
    }
  ]
  
cols = ["user_id:ID","name", "review_count","yelping_since"]

with open('test4.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = cols)
    writer.writeheader()
    writer.writerows(new_dict)


exit()

# file = open("data\yelp_user.json")
# lines_to_print = [0,3]

# for index, line in enumerate(file):
#   if ( index in lines_to_print):
#     print(line)
# file.close()

#import location for json files
data_folder = r"./data"
USER_JSON_FILE = data_folder + "/yelp_user.json"
#export location files
# export_folder = r"/neo4j.import/"

#CONST.
USER_CSV = 'user.csv'
print("\n chemin user.csv : ",USER_CSV, "\n")

def convertForNeo4j():
    with open(USER_JSON_FILE, 'r', encoding='utf-8') as jsonfile:
      with open(USER_CSV, 'w', newline='\n') as csvfile:
        cols = ["user_id:ID","name", "review_count","yelping_since"]
        

        writer = csv.writer(csvfile, fieldnames=cols, delimiter=',', quotechar='"')
        writer.writeheader()
        parser = json.loads(jsonfile)
        writer.writerow(parser)


        lines_to_print = [0,3]
        for index,line in parser: 
          if ( index in lines_to_print):
            print(line) 
        parser.close()
        
        # for i in parser["user_id"]:
        #   print(i)
        # exit()
        #   line = line.strip()
        # if len(line)>0:
        #   exit()
        #   try:
        #   print(type(line))
        #   exit()
        #   json_node = json.load(line)
        #   parser = json.loads(line)
        #   except ValueError:
        #     print("Decoding has failed")

        #   writer.writerow([json_node['user_id'], json_node['name'], json_node['review_count'], json_node['yelping_since']])
        #   print(json_node)
        #   writer.writerow({k:v for k, v in zip(cols, [json_node["user_id"], json_node["name"], 
        #   json_node['review_count'],json_node["yelping_since"], "User"])})

        # with open("neo4j.import\friend.csv", 'w') as friendcsv:
        #   friendwriter = csv.writer(friendcsv, delimiter=',',quotechar='"')
        #   friends_fieldname = [":START_ID(user)",":END_ID(user)"]
        #   friendwriter.writerow(friends_fieldname)

        #   for line in jsonfile:

convertForNeo4j()
