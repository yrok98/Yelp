from py2neo import Graph

# Connection to neo4j databases
SERVER_ADRESSE = "bolt://localhost:7687"
SERVER_AUTH = ("neo4j", "bioinfo")
graph = Graph(SERVER_ADRESSE, auth=SERVER_AUTH)

# CONST. query (use for multiple scores)
q_user = 'match (u:User)-[f:IS_FRIEND_WITH]->(u1:User)-[:HAS_WROTES]->(r:Review)-[w:REVIEWS]->(b:Business) return distinct u.name, u.User;'
q_review_count = 'match (u:User) return distinct u.User, toInteger(u.review_count); '

USERS = graph.run(q_user).to_table()
rCOUNT = graph.run(q_review_count).to_table()

# Dict of user
users = {}
for u in USERS:
    username = u[0]
    user_id = u[1]
    users[user_id] = username


# Centrality Factor
def centralityFactor():
    # Queries
    q_maxFriend = 'match p=(u1:User)-[r:IS_FRIEND_WITH]->(u2:User) with u2, count(u1.User) as nb_friends return max(nb_friends);'
    q_friends = 'match p=(u1:User)-[r:IS_FRIEND_WITH]->(u2:User) with distinct u2, count(u1) as nb_friends RETURN  u2.User, nb_friends ORDER BY u2.name;'

    q_friendsOffriend = 'match p=(u1:User)-[r:IS_FRIEND_WITH]->(u2:User)-[r2:IS_FRIEND_WITH]->(u3:User) with distinct u3, count(u1.User) as nb_friendsOfFriend RETURN u3.User, nb_friendsOfFriend ORDER BY u3.name;'
    q_maxFriendOFfriend = 'match p=(u1:User)-[r:IS_FRIEND_WITH]->(u2:User)-[r2:IS_FRIEND_WITH]->(u3:User) with u3, count(u1.User) as nb_friendsOFfriends return max(nb_friendsOFfriends);'

    q_fans = 'match (u:User) where u.fans <> "0" return distinct u.User, toInteger(u.fans);'
    q_maxFans = 'match (u:User) return u.User, toInteger(u.fans) as fans order by fans DESC limit 1;'

    # run queries in neo4j and get the data
    FRIENDS = graph.run(q_friends).to_table()
    MAXFRIEND = graph.run(q_maxFriend).to_table()
    FRIENDOF = graph.run(q_friendsOffriend).to_table()
    MAXFRIENDOF = graph.run(q_maxFriendOFfriend).to_table()
    FANS = graph.run(q_fans).to_table()
    MAXFANS = graph.run(q_maxFans).to_table()

    # Get max values of friend, friend of friend and fans for a user
    for res in MAXFRIEND:
        populaire = res[0]
        # print(populaire)
    for res in MAXFRIENDOF:
        populaireOfpopulaire = res[0]
        # print(populaireOfpopulaire)
    for res in MAXFANS:
        famous = res[1]
        # print(famous)

    # Get number of friend of each user
    list_friend = {}
    for el in FRIENDS:
        user = el[0]
        nb_friends = el[1]
        list_friend[user] = nb_friends
    # print(list_friend)

    # Get the number of friend of friend for each user
    list_friendOf = {}

    for el in FRIENDOF:
        user = el[0]
        nb_friendOf = el[1]
        list_friendOf[user] = nb_friendOf
    # print(list_friendOf)

    # Get number of fans for each user
    list_fans = {}

    for fan in FANS:
        user = fan[0]
        nb_fans = fan[1]
        list_fans[user] = nb_fans
    # print(list_fans)

    # Score calculation for each users
    centrality = {}
    for u in USERS:
        user_id = u[1]
        if user_id not in list_fans:  # check for user presence in list if not score = 0
            list_fans[user_id] = 0
        if user_id not in list_friendOf:
            list_friendOf[user_id] = 0
        if user_id not in list_friend:
            list_friend[user_id] = 0

        scoreSoc = list_friend[user_id] / populaire
        scoreSocNiv2 = list_friendOf[user_id] / populaireOfpopulaire
        scoreIntrsq = list_fans[user_id] / famous

        # Centrality factor calculation
        scoreCentrality = (scoreSoc + scoreSocNiv2 + scoreIntrsq) / 3
        centrality[user_id] = scoreCentrality
        # print(centrality)

    return (centrality)


def validityFactor():
    q_isUseful = 'match p=(u:User)-[:HAS_WROTES]->(r:Review) where r.useful <> "0" with u, count(r) as amontUseful return distinct u.User, amontUseful;'
    q_isCool = 'match p=(u:User)-[:HAS_WROTES]->(r:Review) where r.cool <> "0" with u, count(r) as amontCool return distinct u.User, amontCool;'
    q_review_count = 'match (u:User) return distinct u.User, toInteger(u.review_count); '

    rCOUNT = graph.run(q_review_count).to_table()
    rUSEFUL = graph.run(q_isUseful).to_table()
    rCOOL = graph.run(q_isCool).to_table()

    # Extract review count for each
    list_rCount = {}
    for review in rCOUNT:
        user = review[0]
        rCount = review[1]
        list_rCount[user] = rCount

    # Extract Useful review for each user
    list_rUseful = {}
    for rev in rUSEFUL:
        user = rev[0]
        rUseful = rev[1]
        list_rUseful[user] = rUseful

    # Extract Cool review for each user
    list_rCool = {}
    for rev in rCOOL:
        user = rev[0]
        rCool = rev[1]
        list_rCool[user] = rCool

    # Score calculation for the validity factor of each user
    validityFactor = {}

    for u in USERS:
        user_id = u[1]

    for u in USERS:
        user_id = u[1]
        if user_id not in list_rCount:  # check for user presence in list if not score = 0
            list_rCount[user_id] = 0
        if user_id not in list_rUseful:
            list_rUseful[user_id] = 0
        if user_id not in list_rCool:
            list_rCool[user_id] = 0

        scoreValidComment = list_rUseful[user_id] / list_rCount[user_id]
        scoreCoolide = list_rCool[user_id] / list_rCount[user_id]

        # ValidityFactor calculation
        scoreValidity = (scoreValidComment + scoreCoolide) / 2  # mean score

        validityFactor[user_id] = scoreValidity

        # print(validityFactor)

    return (validityFactor)


# validityFactor()

def adequacyFactor(ambience, category, priceRange):
    q_ambience = 'match p=(u:User)-[:HAS_WROTES]->(r:Review)-[:REVIEWS]->(b:Business)-[:IN_AMBIENCE]->(a:Ambience) where toInteger(r.stars) >= 4 with u, count(r) as reviewPos, a return u.User, reviewPos, a.Ambience ;'
    q_categorie = 'match p=(u:User)-[:HAS_WROTES]->(r:Review)-[:REVIEWS]->(b:Business)-[:IN_CATEGORY]->(c:Categories) where toInteger(r.stars) >= 4 with u, count(r) as reviewPos, c return u.User, reviewPos, c.Categories;'
    q_price = 'match p=(u:User)-[:HAS_WROTES]->(r:Review)-[:REVIEWS]->(b:Business) where toInteger(r.stars) >= 4 with u, count(r) as reviewPos, toInteger(b.priceRange) as PriceRange return distinct u.User, reviewPos, PriceRange;'

    AMBIENCE = graph.run(q_ambience).to_table()
    CATEGORY = graph.run(q_categorie).to_table()
    PRICE = graph.run(q_price).to_table()

    m = len(ambience)
    n = len(category)

    # Extract review count for each
    list_rCount = {}

    for review in rCOUNT:
        user = review[0]
        rCount = review[1]
        list_rCount[user] = rCount
    # print(list_rCount)

    # Calcul categorie adequacy score
    list_catAdequacy = {}

    for el in CATEGORY:
        user = el[0]
        curr_cat = el[2]
        reviewPos = el[1]
        # print(curr_cat,list_rCount[user])

        if curr_cat in category:
            scoreCategory = (reviewPos / list_rCount[user]) / n
            list_catAdequacy[user] = scoreCategory  # stock user values in dict

    # Calcul ambience adequacy score
    list_ambAdequacy = {}

    for el in AMBIENCE:
        user_id = el[0]
        amb = el[2]
        reviewPos = el[1]

        if amb in ambience:
            scoreAmbience = (reviewPos / list_rCount[user_id]) / m
            list_ambAdequacy[user_id] = scoreAmbience

            # Calcul price range adequacy score
    list_priceAdequacy = {}

    for el in PRICE:
        user_id = el[0]
        priceR = el[2]
        reviewPos = el[1]

        if priceR == priceRange:
            scorePrice = reviewPos / list_rCount[user_id]
            list_priceAdequacy[user_id] = scorePrice

            # Adequacy score of each user
    adequacy = {}
    for u in USERS:
        user_id = u[1]
        if user_id not in list_ambAdequacy:  # check for user presence in list if not score = 0
            list_ambAdequacy[user_id] = 0
        if user_id not in list_catAdequacy:
            list_catAdequacy[user_id] = 0
        if user_id not in list_priceAdequacy:
            list_priceAdequacy[user_id] = 0

        scoreAdequacyFactor = (list_ambAdequacy[user_id] + list_catAdequacy[user_id] + list_priceAdequacy[user_id]) / 3

        adequacy[user_id] = scoreAdequacyFactor

    return (adequacy)


def geoFactor(city):
    q_reviewFriendCity = 'match p=(u:User)-[:IS_FRIEND_WITH]->(u2:User)-[:HAS_WROTES]->(r:Review)-[:REVIEWS]->(b:Business)-[:IN_CITY]->(c:City) with u, count(r) as reviewFriend, c return distinct u.User, reviewFriend, c.City order by u.User;'
    q_reviewF = 'match p=(u:User)-[:IS_FRIEND_WITH]->(u2:User)-[:HAS_WROTES]->(r:Review)-[:REVIEWS]->(b:Business) with u, count(r) as reviewFriend return distinct u.User, reviewFriend order by u.User; '

    REVFRIEND = graph.run(q_reviewFriendCity).to_table()
    REV_TOTAL = graph.run(q_reviewF).to_table()

    list_revTotal = {}

    for rev in REV_TOTAL:
        user_id = rev[0]
        revTotal = rev[1]
        list_revTotal[user_id] = revTotal

    list_revFriendCity = {}
    for rev in REVFRIEND:
        user_id = rev[0]
        revFriendCity = rev[1]
        curr_city = rev[2]

        if curr_city in city:
            list_revFriendCity[user_id] = revFriendCity

    geo = {}  # geographic factor of each user
    for u in USERS:
        user_id = u[1]
        if user_id not in list_revFriendCity:  # check for user presence in list if not score = 0
            list_revFriendCity[user_id] = 0
        if user_id not in list_revTotal:
            list_revTotal[user_id] = 0

        geo[user_id] = list_revFriendCity[user_id] / list_revTotal[user_id]

    return (geo)


# Calcul final 'score d'influence' for each user depending on restaurant caracteristics
def userScore(city, ambience, category, price):
    alpha = 0.3
    beta = 0.3
    gamma = 0.3
    delta = 0.1

    scoreFinal = {}

    centralityF = centralityFactor()
    validityF = validityFactor()
    adequacyF = adequacyFactor(ambience, category, price)
    geographicF = geoFactor(city)

    for d in (centralityF, validityF, adequacyF, geographicF):

        for id, v in d.items():
            scoreFinal[id] = (alpha * centralityF[id]) + (beta * validityF[id]) + (gamma * adequacyF[id]) + (
                    delta * geographicF[id])

    # Sorted users depending on score
    final = dict(sorted(scoreFinal.items(), key=lambda x: x[1], reverse=True))

    print(f'\n\n Les 10 utilisateurs à invité pour un restaurant à', *city, ", dont l'ambiance est ", *ambience,
          ", du type ", *category, ", dans une gamme ", price, " de prix sont : \n\n")

    # OUTPUT
    print('           {}\t                {}\t\n'.format('ID', 'SCORE'))
    for i in range(10):
        print("{}\t{}\t".format(list(final.keys())[i], list(final.values())[i]))


if __name__ == '__main__':
    # TESTS
    userScore(['Wilmington'], ['casual'], ['Pizza', 'Burgers', 'Italian'], 1)
    userScore(['Wilmington'], ['casual', 'romantic'], ['Chinese'], 2)
    userScore(['Wilmington'], ['hipster'], ['Nightlife', 'Bars'], 1)
    userScore(['New Castle'], ['casual', 'classy'], ['Coffee & Tea'], 2)
    userScore(['New Castle'], ['classy'], ['Seafood'], 1)
