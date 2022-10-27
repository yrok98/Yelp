import json
import csv
from matplotlib.font_manager import json_load
import pandas as pd
import re
import ast

#FILE CONSTANT
USER_JSON_FILE = open("data/yelp_user.json")
REVIEW_JSON_FILE = open("data/yelp_review.json")
BUSINESS_JSON_FILE = open("data/yelp_restaurants.json")

#COLNAMES FOR RELATION FILE
RELATION_COLNAMES = [":START_ID", ":END_ID", ":TYPE"]
BUSINESS_COLNAMES = [":ID(Business)", ":LABEL","name"]
USER_COLNAMES = ['User:ID(User)',':LABEL','name','review_count','yelping_since','useful', 'fans','average_stars']
REVIEW_COLNAMES = ['Review:ID(Review)', ':LABEL', 'stars', 'useful','cool','text']
CATEGORIES_COLNAMES = ['Categories:ID(Categories)', ":LABEL"]
CITY_COLNAMES= ['City:ID(City)', ':LABEL']

#write user node
def user_node(): 
    with open('data/yelp_user.json', 'r') as f: 
        with open('neo4j.nodes/user.csv', 'w', encoding ='UTF-8',newline='') as wf: 
            col_headers=USER_COLNAMES
            w = csv.writer(wf)
            data = json.load(f)

            w.writerow(col_headers)
            for i in data:
                w.writerow([i['user_id'],'User',i['name'], i["review_count"], i["yelping_since"],i["useful"], i["fans"],i['average_stars']])
        wf.close()
    f.close()

categories_nodes = set()

# #write business node
def business_node(): 
    with open('data/yelp_restaurants.json', 'r') as f: 
            business_data = json.load(f)

            with open("neo4j.nodes/business.csv", 'w', encoding ='UTF-8', newline='') as wf:
                w=csv.writer(wf)
                w.writerow(['Business:ID(Business)',':LABEL', 'name', 'priceRange'])

                for i in business_data:
                    attributs = i['attributes']
                    if attributs is not None :
                        if 'RestaurantsPriceRange2' in attributs:
                            price = attributs['RestaurantsPriceRange2'].strip()
                        else:
                            price = None
                        w.writerow([i['business_id'], 'Business', i['name'], price])
business_node()
exit()
#write category node
def categories():
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
                w.writerow([category, 'Categories']) # ajout au fichier csv la categorie si elle est nouvelle.

    #check for duplicated word 
        # df = pd.DataFrame(open('neo4j.nodes/categories.csv'))
        # df.duplicated(subset=None, keep='first')
    f.close()

#write city node 
def city(): 
    with open('neo4j.nodes/city.csv', 'w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)

        data= json.load(open('data/yelp_restaurants.json'))
        w.writerow(CITY_COLNAMES)

        seen = []

        for item in data:
            city = item['city'].strip(', ')
            city = city[0].upper()+city[1:] #duplicate with lower/upper case on first letter (Willington =! willington)
            # for city in line: 
            if city in seen:
                continue
            seen.append(city)
            w.writerow([city, 'City'])
    f.close()

#check for duplicate
df = pd.read_csv('neo4j.nodes/city.csv')
df.duplicated(subset=None, keep='first')
df.to_csv('neo4j.nodes/city.csv', index=None)

# #write friend relationship
def friends():
        with open("neo4j.relationship/is_friend_with.csv", 'w', encoding ='UTF-8', newline='') as f:
            data = json.load(USER_JSON_FILE)

            w=csv.writer(f)
            w.writerow([':START_ID(User)', ':END_ID(User)', ':TYPE'])

            for i in data:
                # print(i['friends'])
                while i['friends']: 
                    curr_friend = i['friends'].pop()
                    #(User)-[IS_FRIEND_WITH]->(User)
                    w.writerow([i['user_id'], curr_friend, 'IS_FRIEND_WITH'])

        f.close()

# write in_categories relationship
def in_category():
    with open('neo4j.relationship/in_category.csv', 'w', newline='', encoding='utf-8') as csvfile:
        with open('data/yelp_restaurants.json', 'r') as jsonfile:
            w = csv.writer(csvfile)
            w.writerow([':START_ID(Business)', ':END_ID(Categories)', ':TYPE'])
        
            json_resto = json.load(jsonfile)
            
            #print(len(line['categories'].strip())>0)

            for line in json_resto:
                # categories = line['categories'].split(', ')
                if line['categories'] and len(line['categories'].strip()) > 0:
                    cur_categories = list(map(lambda x: x.strip(), re.split('\s*,\s*', line['categories'].strip())))

    #               print(cur_categories)
                    for category in cur_categories:
                        # print(category)
                        w.writerow([line['business_id'], category, 'IN_CATEGORY'])
                
#write in_city relationship 
def in_city():
    with open('neo4j.relationship/in_city.csv', 'w', newline='', encoding='utf-8') as csvfile:
        with open('data/yelp_restaurants.json', 'r') as jsonfile:
            w = csv.writer(csvfile)
            w.writerow([':START_ID(Business)', ':END_ID(City)', ':TYPE'])
            
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

def ambience():
    with open('neo4j.nodes/ambience.csv', 'w', newline='', encoding='utf-8') as f, open('relation.csv', 'w', newline='', encoding='utf-8') as r:
        w = csv.writer(f)
        
        json_data = json.load(open('data/yelp_restaurants.json'))
        
        w.writerow(['Ambience:ID(Ambience)', ':LABEL'])
        amb_list =[]

        for item in json_data :
            attribut = item['attributes']
            if attribut is not None:
                if 'Ambience' in attribut :
                    amb = ast.literal_eval(attribut['Ambience'])
                    if amb is not None:
                        for k,v in amb.items():
                            if v == True : 
                                if k not in amb_list:
                                    w.writerow([k, 'Ambience'])
                                    amb_list.append(k)

# Relation business_id / Ambience
def in_ambience(): 
    with open('neo4j.relationship/in_ambience.csv', 'w', newline='', encoding='utf-8') as file: 
        jsondata = json.load(open('data/yelp_restaurants.json'))
        
        w = csv.writer(file)
        w.writerow([':START_ID(Business)', ':END_ID(Ambience)', ':TYPE'])
        
        for i in jsondata: 
            attribut = i['attributes']
            if attribut is not None:
                if 'Ambience' in attribut:
                    amb = ast.literal_eval(attribut['Ambience'])
                    if amb is not None: 
                        for k,v in amb.items():
                            if v == True : 
                                #(Business)-[IN_AMBIENCE]->(Ambience)
                                w.writerow([i['business_id'], k, 'IN_AMBIENCE'])

#write review relationship (wrotes, reviews)
def review():
    with open("data/yelp_review.json", "r") as f:
        with open('neo4j.nodes/review.csv', 'w', newline='', encoding='utf-8') as csvfile:
            data = json.load(f)
            w = csv.writer(csvfile)
            w.writerow(REVIEW_COLNAMES)

        
            for line in data:
                w.writerow([line['review_id'], 'Review', line['stars'], line['useful'], line['cool'], line['text'].replace('\n', ' ').replace('\n', ' ').replace('"', '').replace('\\', '')])
            # print(type(line['text']))

def review_relationships(): 
    with open('neo4j.relationship/has_wrotes.csv', 'w', newline='', encoding='utf-8') as f_user, open('neo4j.relationship/reviews.csv', 'w', newline='', encoding='utf-8') as f_bus:
        rev = json.load(open('data/yelp_review.json'))
        w_user=csv.writer(f_user)
        w_bus=csv.writer(f_bus)

        w_user.writerow([':START_ID(User)', ':END_ID(Review)', ':TYPE'])
        w_bus.writerow([':START_ID(Review)', ':END_ID(Business)', ':TYPE'])

        for i in rev: 
            #(User)-[HAS_WROTE]->(Review)
            w_user.writerow([i['user_id'], i['review_id'], 'HAS_WROTES'])

            #(Review)-[REVIEWS]->(Business)
            w_bus.writerow([i['review_id'], i['business_id'], 'REVIEWS'])
        f_user.close()
        f_bus.close()


review()

exit()
in_ambience()
review()
user_node()
business_node()
categories()
city()
friends()
in_category()
in_city()
ambience()
in_ambience()
review_relationships()
