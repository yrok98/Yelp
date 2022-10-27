from py2neo import Graph


#Connection to neo4j db
SERVER_ADRESSE = "bolt://localhost:7687"
SERVER_AUTH = ("neo4j", "bioinfo")
graph = Graph(SERVER_ADRESSE, auth=SERVER_AUTH)


q = "match (u:User) return u.name as username"
res = graph.run(q).to_table()
for record in res :
    print(record[0])