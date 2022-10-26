import json
import csv
import pandas as pd
import re

#FILE CONSTANT
USER_JSON_FILE = open("data/yelp_user.json")
REVIEW_JSON_FILE = open("data/yelp_review.json")
BUSINESS_JSON_FILE = open("data/yelp_restaurants.json")

#COLNAMES FOR RELATION FILE
RELATION_COLNAMES = [":START_ID", ":END_ID", ":TYPE"]
BUSINESS_COLNAMES = [":ID(Business)", ":LABEL","name"]
USER_COLNAMES = [":ID(User)",":LABEL","name","review_count","yelping_since","useful", "fans","average_stars"]
REVIEW_COLNAMES = [':ID(Review)', ':LABEL', 'stars:int', 'useful:int','text']
CATEGORIES_COLNAMES = [':ID(Categories)', ":LABEL"]
CITY_COLNAMES= [':ID(City)', ':LABEL']

#write user node
def user_node(): 
    with open('data/yelp_user.json', 'r') as f: 
        with open('neo4j.nodes/user.csv', 'w', encoding ='UTF-8',newline='') as wf: 
            col_headers=USER_COLNAMES
            w = csv.writer(wf)
            data = json.load(f)

            w.writerow(col_headers)
            for i in data:
                w.writerow([i['user_id'],"User",i['name'], i["review_count"], i["yelping_since"],i["useful"], i["fans"],i['average_stars']])
        wf.close()
    f.close()

categories_nodes = set()

# #write business node
def business_node(): 
    with open('data/yelp_restaurants.json', 'r') as f: 
        business_data = json.load(f)

        with open("neo4j.nodes/business_test.csv", 'w', encoding ='UTF-8', newline='') as wf:
            w=csv.writer(wf)
            w.writerow(BUSINESS_COLNAMES)

            for i in business_data:
                w.writerow([i['business_id'], 'Business', i['name']])

        wf.close()
    f.close()


#write category node
def categories_nodes():
    with open('neo4j.nodes/categories.csv', 'w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)

        data = json.load(BUSINESS_JSON_FILE)
        w.writerow(CATEGORIES_COLNAMES)

        seen = [] #list pour enregister les categories deja rencontre

        for item in data: 
            line = item['categories'].split(', ') # 1 ligne = plusieurs categories
            for category in line: #prend les category dans la ligne
                if category in seen: # check pour une nouvelle categorie est connue
                    continue
                seen.append(category) #ajout categorie a la liste des categories connues
                w.writerow([category, 'Category']) # ajout au fichier csv la categorie si elle est nouvelle.

    #check for duplicated word 
        # df = pd.DataFrame(open('neo4j.nodes/categories.csv'))
        # df.duplicated(subset=None, keep='first')
    f.close()


#write city node 
def city_node(): 
    with open('neo4j.nodes/city_test.csv', 'w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)

        data= json.load(BUSINESS_JSON_FILE)
        w.writerow(CITY_COLNAMES)

        seen = []

        for item in data:
            city = item['city']
            print(city)
            # for city in line: 
            if city in seen:
                continue
            seen.append(city)
            w.writerow([city, 'City'])
    f.close()

# #write friend relationship
def friend_relationship():
        with open("neo4j.relationship/friend_relationship.csv", 'w', encoding ='UTF-8', newline='') as f:
            w=csv.writer(f)
            w.writerow(RELATION_COLNAMES)
            for i in data:
                if i['friends']: 
                    w.writerow([i['user_id'], i['friends'], 'IS_FRIEND_WITH'])
        f.close()

# write in_categories relationship
def in_category():
    with open('neo4j.relationship/in_category.csv', 'w', newline='', encoding='utf-8') as csvfile:
        with open('data/yelp_restaurants.json', 'r') as jsonfile:
            w = csv.writer(csvfile)
            w.writerow([':ID(categories)', ':LABEL'])
        
            json_resto = json.load(jsonfile)
            
            #print(len(line['categories'].strip())>0)

            for line in json_resto:
                categorie = line['categories'].split(', ')
                if line['categories'] and len(line['categories'].strip()) > 0:
                    cur_categories = list(map(lambda x: x.strip(), re.split('\s*,\s*', line['categories'].strip())))

    #               print(cur_categories)
                    for category in cur_categories:
                        # print(category)
                        w.writerow([line['business_id'], category, 'IN_CATEGORY'])
                


#write in_price_range relationship ===========================> TO DO


#write in_city relationship ===========================> TO DO

with open('neo4j.relationship/in_city.csv', 'w', newline='', encoding='utf-8') as csvfile:
    with open('data/yelp_restaurants.json', 'r') as jsonfile:
        w = csv.writer(csvfile)
        w.writerow([':ID(city)', ':LABEL'])
        
        json_resto = json.load(open('data/yelp_restaurants.json'))
        
        #             print(len(line['categories'].strip())>0)

        for line in json_resto:
            city = line['city'].split(', ')
            if line['city'] and len(line['city'].strip()) > 0:
                cur_city = list(map(lambda x: x.strip(), re.split('\s*,\s*', line['city'].strip())))

#                 print(cur_city)
                for city in cur_city:
                    w.writerow([line['business_id'], city, 'IN_CITY'])
                    # print(city)


#write in_ambiance relationship ==========================> TO DO


#write ambiance nodes =================================> TO DO


#write review relationship (wrotes, reviews)
with open("data/yelp_review.json", "r") as f:
    with open('neo4j.nodes/review.csv', 'w', newline='', encoding='utf-8') as csvfile:
        data = json.load(f)
        w = csv.writer(csvfile, escapechar="\\", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(REVIEW_COLNAMES)

    
        for line in data:
            w.writerow([line['review_id'], 'Review', line['stars'], line['useful'], line['text'].replace('\n', ' ').replace('\n', ' ').replace('"', '').replace('\\', '')])
        # print(type(line['text']))


def review_relationships(): 
    with open('neo4j.relationship/has_wrotes.csv', 'w', newline='', encoding='utf-8') as f_user, open('neo4j.relationship/reviews.csv', 'w', newline='', encoding='utf-8') as f_bus:
        rev = json.load(open('data/yelp_review.json'))
        w_user=csv.writer(f_user)
        w_bus=csv.writer(f_bus)

        w_user.writerow(RELATION_COLNAMES)
        w_bus.writerow(RELATION_COLNAMES)

        for i in rev: 
            #(User)-[HAS_WROTE]->(Review)
            w_user.writerow([i['user_id'], i['review_id'], 'HAS_WROTES'])

            #(Review)-[REVIEWS]->(Business)
            w_bus.writerow([i['review_id'], i['business_id'], 'REVIEWS'])
        f_user.close()
        f_bus.close()


