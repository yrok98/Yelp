import json
import pandas as pd
import csv


#FILE CONSTANT
USER_JSON_FILE = open("data/yelp_user.json", 'r')
REVIEW_JSON_FILE = open("data/yelp_review.json")
RESTO_JSON_FILE = open("data/yelp_restaurants.json")

#COLNAMES FOR RELATION FILE
RELATION_COLNAMES = [":START_ID(user)", ":END_ID(user)"]
RESTO_COLNAMES = ['business_id:ID', 'name']

#READ JSON 
# user_json = pd.read_json(USER_JSON_FILE)
# friends = user_json['friends']
# review_json = pd.read_json(REVIEW_JSON_FILE)

#write user node
# with open('data/yelp_user.json', 'r') as f: 
#     with open('neo4j.data/user.csv', 'w', encoding ='UTF-8',newline='') as wf: 
#         col_headers=["user_id:ID(user)","name","review_count","yelping_since","useful", "fans","average_stars"]
#         w = csv.writer(wf)
#         data = json.load(f)

#         w.writerow(col_headers)
#         for i in data:
#             # print(i['user_id'])
#             w.writerow([i['user_id'], 
#                         i['name'], 
#                         i["review_count"], 
#                         i["yelping_since"], 
#                         i["useful"], 
#                         i["fans"], 
#                         i['average_stars']])
#         # df = pd.DataFrame(w)
#         # df.to_csv('data2/test_user.csv', index=False)
#         f.close()

# #write friend relationship file
#         with open("neo4j.data/friend_relationship.csv", 'w', encoding ='UTF-8', newline='') as f:
#             w=csv.writer(f)
#             w.writerow(RELATION_COLNAMES)
#             for i in data:
#                 # print(i['friends'])
#                 if i['friends']: 
#                     w.writerow([i['user_id'], i['friends']])
#             f.close()

#write restaurant nodes
with open('data/yelp_restaurants.json', 'r') as f: 
    resto_data = json.load(f)
    with open("neo4j.data/resto.csv", 'w', encoding ='UTF-8', newline='') as wf:
     w=csv.writer(wf)
     w.writerow(RELATION_COLNAMES)

     for i in resto_data:
        w.writerow([i['business_id'], i['name']])

#write review relationship (wrotes, reviews)
with (open('neo4j.data/wrotes.csv', 'w', newline='', encoding='utf-8')) as f_user, open('neo4j.data/reviews.csv', 'w', newline='', encoding='utf-8') as f_bus:
    rev = json.load(open('data/yelp_review.json'))
    w_user=csv.writer(f_user)
    w_bus=csv.writer(f_bus)
    w_user.writerow(RELATION_COLNAMES)
    w_bus.writerow(RELATION_COLNAMES)

    for i in rev: 
        w_user.writerow([i['user_id'], i['review_id']])
        w_bus.writerow([i['review_id'], i['business_id']])
    f.close()

#
exit()

with open('data/yelp_review.json') as f:
    w = csv.writer()
    data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv('data2/test_rev.csv', index=False)

    for i in data:
        print(i['review_id'])
    f.close()

exit()
user_load = json.load(USER_JSON_FILE)
print(user_load)
exit()

#OTHERS CONSTANTS
USER_COLNAMES = ["user_id", "name", "review_count","useful", "cool", "fans","average_stars"]
REVIEW_COLNAMES = ["review_id","user_id","business_id",
                    "stars","useful","text","date" ]

#RENAME COLNAMES FOR FILES


# review_json = pd.read_json(REVIEW_JSON_FILE)
# print(review_json['review_id'])

# with open("data/yelp_review.json", 'r') as json_file:
#     json_data = json_load(json_file)

#     data_file = open("data2/review_test.csv", "w", newline='' )
#     csv_writer = csv.writer()

# with open("data2/review_test.csv", "w", encoding='utf-8', newline='') as outputfile:
#     w = csv.writer(outputfile, delimiter=",")
#     for item in review_json:

#         print(type(item))
#         # w.writerow()


# #Double quote 
# def doublequote(str):
#     json.dumps(str)





# for text in review_json['text']:
#     if text is not None:
#         str(text).


# review_json.to_csv("data2/review.csv", index=False, columns=REVIEW_COLNAMES, header=["review_id:ID","user_id","business_id",
#                     "stars","useful","text","date"])

exit()
#RELATIONSHIP
user_friend = pd.concat([user_json['user_id'], friends], axis=1)
user_friend.to_csv("data2/friend.csv", index=False, header=RELATION_COLNAMES)

#NODES
user_json.to_csv("data2/user.csv", index=None, columns=USER_COLNAMES, header=["user_id:ID(user)", "name", "review_count","useful", "cool", "average_stars"])

exit()




