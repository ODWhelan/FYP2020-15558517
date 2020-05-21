import db_connect
import json

with open("node_data_out.json") as f:
    data = json.load(f)
f.close()

location = db_connect.DatabaseConnector("mongodb://localhost:27017", "Meta", "Locations")
leaves = db_connect.DatabaseConnector("mongodb://localhost:27017", "Meta", "End Nodes")
for node in data["Sheet1"]:
    if node["children"] != 0:
        record = {"node_id": node["node_id"], "parent_node_id": node["parent_node_id"], "name": node["name"],
                  "child_nodes": node["child_nodes"], "children": node["children"]}
        location.insert_record(record)
    else:
        record = {"node_id": node["node_id"], "parent_node_id": node["parent_node_id"], "name": node["name"], "utility":
                  node["utility"], "units": node["unit_label"], "earliest_data": None}
        leaves.insert_record(record)
