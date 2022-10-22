
import csv
import json
import re
from typing import Set, Tuple

from converter_json_ver1 import write_user_nodes

FRIENDS = 'FRIENDS'

user_json_file = "data\yelp_user.json"

user_nodes_csv_file = "user_nodes.csv"

relationship_csv_file = "relationships.csv"

# Relationship writer
relationship_csv = open(relationship_csv_file, mode="w", encoding="utf-8", newline="\n")
relationship_fieldnames = [":START_ID", ":END_ID", ":TYPE"]
relationship_writer = csv.DictWriter(relationship_csv, fieldnames=relationship_fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
relationship_writer.writeheader()

friend_relationships: Set[Tuple[str, str, str]] = set()

def writer_user_nodes_csv():
    with open(user_json_file, "r", encoding="utf-8") as ujf, open(user_nodes_csv_file, mode="w", encoding="utf-8", newline="\n") as user_nodes_csv:
        fieldnames = ["user_id:ID", "name", "yelping_since", ":LABEL"]
        writer = csv.DictWriter(user_nodes_csv, fieldnames=fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

    for line in ujf:
                    line = line.strip()
                    if len(line)>0:
                        json_node = json.loads(line)
                        writer.writerow({k:v for k, v in zip(fieldnames, [json_node["user_id"], json_node["name"], json_node["yelping_since"], USER_NODE])})
                        if json_node["friends"] and len(json_node["friends"].strip()) > 0:
                            friends_arr = re.split("\s*,\s*", json_node["friends"].strip())
                            for friend_id in friends_arr:
                                # Prevent duplicate friend relationship later!
                                f1 = min(json_node["user_id"], friend_id)
                                f2 = max(json_node["user_id"], friend_id)
                                friend_relationships.add((f1, f2, FRIENDS))

    for (f1, f2, rel_type) in friend_relationships:
                relationship_writer.writerow({k:v for k, v in zip(relationship_fieldnames, [f1, f2, rel_type])})

writer_user_nodes_csv()
