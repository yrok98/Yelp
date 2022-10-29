import json
import csv
import re
import ast

# IMPORT FILES CONSTANT
USER_JSON_FILE = "data/yelp_user.json"
REVIEW_JSON_FILE = "data/yelp_review.json"
BUSINESS_JSON_FILE = "data/yelp_restaurants.json"

# OUTPUT FILES CONSTANT
node_repo = "neo4j.nodes/"
USER_CSV = node_repo + "user.csv"
BUSINESS_CSV = node_repo + "business.csv"
AMBIENCE_CSV = node_repo + "ambience.csv"
CITY_CSV = node_repo + "city.csv"
REVIEW_CSV = node_repo + "review.csv"
CATEGORIES_CSV = node_repo + "categories.csv"

rel_repo = "neo4j.relationship/"
HAS_WROTES_CSV = rel_repo + "has_wrotes.csv"
IN_AMBIENCE_CSV = rel_repo + "in_ambience.csv"
IN_CATEGORY_CSV = rel_repo + "in_category.csv"
IN_CITY_CSV = rel_repo + "in_city.csv"
IS_FRIEND_WITH_CSV = rel_repo + "is_friend_with.csv"
REVIEWS_CSV = rel_repo + "reviews.csv"

# COLNAMES NODE
RELATION_COLNAMES = [":START_ID", ":END_ID", ":TYPE"]

USER_COLNAMES = ['User:ID(User)', ':LABEL', 'name', 'review_count', 'yelping_since', 'useful', 'fans', 'average_stars']
BUSINESS_COLNAMES = ['Business:ID(Business)', ':LABEL', 'name', 'priceRange']
REVIEW_COLNAMES = ['Review:ID(Review)', ':LABEL', 'stars', 'useful', 'cool', 'text']
CATEGORIES_COLNAMES = ['Categories:ID(Categories)', ":LABEL"]
CITY_COLNAMES = ['City:ID(City)', ':LABEL']

AMBIENCE_COLNAMES = ['Ambience:ID(Ambience)', ':LABEL']

# COLNAMES RELATION
CATEGORIES_RELATION = [':START_ID(Business)', ':END_ID(Categories)', ':TYPE']
FRIEND_RELATION = [':START_ID(User)', ':END_ID(User)', ':TYPE']
CITY_RELATION = [':START_ID(Business)', ':END_ID(City)', ':TYPE']
AMBIENCE_RELATION = [':START_ID(Business)', ':END_ID(Ambience)', ':TYPE']
USER_REV_RELATION = [':START_ID(User)', ':END_ID(Review)', ':TYPE']
BUSINESS_REV_RELATION = [':START_ID(Review)', ':END_ID(Business)', ':TYPE']
CATEGORIES_RELATION = [':START_ID(Business)', ':END_ID(Categories)', ':TYPE']


# write user node csv to csv
def user_node():
    with open(USER_JSON_FILE, 'r') as f:
        with open(USER_CSV, 'w', encoding='UTF-8', newline='') as wf:
            w = csv.writer(wf)
            data = json.load(f)

            w.writerow(USER_COLNAMES)
            for i in data:
                w.writerow(
                    [i['user_id'], 'User', i['name'], i["review_count"], i["yelping_since"], i["useful"], i["fans"],
                     i['average_stars']])


# #write business node to csv
def business_node():
    with open(BUSINESS_JSON_FILE, 'r') as f:
        business_data = json.load(f)

        with open(BUSINESS_CSV, 'w', encoding='UTF-8', newline='') as wf:
            w = csv.writer(wf)
            w.writerow(BUSINESS_COLNAMES)

            for i in business_data:
                attributs = i['attributes']  # nested dict 'attributes' data
                price = None
                if attributs is not None:  # check for attributes
                    if 'RestaurantsPriceRange2' in attributs:  # check for attribute RestaurantsPriceRange2 in attributes nested dict
                        price = attributs['RestaurantsPriceRange2'].strip()
                w.writerow([i['business_id'], 'Business', i['name'], price])


# write category node
def categories_node():
    with open(CATEGORIES_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)

        data = json.load(open(BUSINESS_JSON_FILE))
        w.writerow(CATEGORIES_COLNAMES)

        seen = []  # list of categories

        for item in data:
            line = item['categories'].split(', ')  # 1 line = multiples categories
            for category in line:
                if category in seen:  # check known categories
                    continue
                seen.append(category)  # add new category to the known categories list
                w.writerow([category, 'Categories'])

            # write city node


def city_node():
    with open(CITY_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)

        data = json.load(open(BUSINESS_JSON_FILE))
        w.writerow(CITY_COLNAMES)

        seen = []  # list of city

        for item in data:
            city = item['city'].strip(', ')
            city = city[0].upper() + city[
                                     1:]  # duplicate with lower/upper case on first letter (Willington =! willington)
            if city in seen:
                continue
            seen.append(city)
            w.writerow([city, 'City'])


# write ambience node
def ambience_node():
    with open(AMBIENCE_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)

        json_data = json.load(open(BUSINESS_JSON_FILE))

        w.writerow(AMBIENCE_COLNAMES)
        amb_list = []  # list of ambience

        for item in json_data:
            attribut = item['attributes']  # nested dict again
            if attribut is not None:
                if 'Ambience' in attribut:  # check for ambience attribute
                    amb = ast.literal_eval(attribut['Ambience'])  # transforme   string dict -> dict
                    if amb is not None:
                        for k, v in amb.items():
                            if v == True:
                                if k not in amb_list:
                                    w.writerow([k, 'Ambience'])
                                    amb_list.append(k)


# write review relationship (wrotes, reviews)
def review_node():
    with open(REVIEW_JSON_FILE, "r") as f:
        with open(REVIEW_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            data = json.load(f)
            w = csv.writer(csvfile)

            w.writerow(REVIEW_COLNAMES)

            for line in data:
                w.writerow([line['review_id'], 'Review', line['stars'], line['useful'], line['cool'],
                            line['text'].replace('\n', ' ').replace('\n', ' ').replace('"', '').replace('\\', '')])


# #write friend relationship
def friends_relation():
    with open(IS_FRIEND_WITH_CSV, 'w', encoding='UTF-8', newline='') as f:
        data = json.load(open(USER_JSON_FILE))

        w = csv.writer(f)
        w.writerow(FRIEND_RELATION)

        for i in data:
            while i['friends']:  # friends = list
                curr_friend = i['friends'].pop()  # take one out of the list
                # (User)-[IS_FRIEND_WITH]->(User)
                w.writerow([i['user_id'], curr_friend, 'IS_FRIEND_WITH'])


# write in_categories relationship
def in_category():
    with open(IN_CATEGORY_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        with open(BUSINESS_JSON_FILE, 'r') as jsonfile:
            w = csv.writer(csvfile)
            w.writerow(CATEGORIES_RELATION)

            json_resto = json.load(jsonfile)

            for line in json_resto:
                if line['categories'] and len(line['categories'].strip()) > 0:
                    cur_categories = list(map(lambda x: x.strip(), re.split('\s*,\s*', line['categories'].strip())))
                    # from internet ... it's works, i don't know why ¯\_(ツ)_/¯

                    for category in cur_categories:
                        # (Business)-[IN_CATEGORY]->(Category)
                        w.writerow([line['business_id'], category, 'IN_CATEGORY'])


# write in_city relationship
def in_city():
    with open(IN_CITY_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(CITY_RELATION)

        json_resto = json.load(open(BUSINESS_JSON_FILE))

        for line in json_resto:
            city = line['city'].split(', ')
            if line['city'] and len(line['city'].strip()) > 0:
                cur_city = list(map(lambda x: x.strip(), re.split('\s*,\s*', line['city'].strip())))  # ¯\_(ツ)_/¯

                #                 print(cur_city)
                for city in cur_city:
                    # (Business)-[IN_CITY]->(City)
                    w.writerow([line['business_id'], city, 'IN_CITY'])


# Relation business_id / Ambience
def in_ambience():
    with open(IN_AMBIENCE_CSV, 'w', newline='', encoding='utf-8') as file:
        jsondata = json.load(open(BUSINESS_JSON_FILE))

        w = csv.writer(file)
        w.writerow(AMBIENCE_RELATION)

        for i in jsondata:
            attribut = i['attributes']  # the one and only nested dict
            if attribut is not None:
                if 'Ambience' in attribut:
                    amb = ast.literal_eval(attribut['Ambience'])
                    if amb is not None:
                        for k, v in amb.items():
                            if v:
                                # (Business)-[IN_AMBIENCE]->(Ambience)
                                w.writerow([i['business_id'], k, 'IN_AMBIENCE'])


def review_relation():
    with open(HAS_WROTES_CSV, 'w', newline='', encoding='utf-8') as f_user, open('neo4j.relationship/reviews.csv', 'w',
                                                                                 newline='', encoding='utf-8') as f_bus:
        rev = json.load(open(REVIEW_JSON_FILE))
        w_user = csv.writer(f_user)
        w_bus = csv.writer(f_bus)

        w_user.writerow(USER_REV_RELATION)
        w_bus.writerow(BUSINESS_REV_RELATION)

        for i in rev:
            # (User)-[HAS_WROTE]->(Review)
            w_user.writerow([i['user_id'], i['review_id'], 'HAS_WROTES'])

            # (Review)-[REVIEWS]->(Business)
            w_bus.writerow([i['review_id'], i['business_id'], 'REVIEWS'])


if __name__ == '__main__':
    # CREATE NODES CSV
    user_node()
    business_node()
    ambience_node()
    city_node()
    review_node()
    categories_node()

    # CREATE RELATIONSHIP CSV
    friends_relation()
    in_ambience()
    in_category()
    in_city()
    review_relation()
