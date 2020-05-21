import json

with open("node_data.json") as f:
    data = json.load(f)
f.close()

nodes = 0
indeces = []
jndeces = []

i = 0
for node in data["Sheet1"]:
    data["Sheet1"][i]["child_nodes"] = []
    data["Sheet1"][i]["children"] = 0
    nodes += 1
    if node["parent_node_id"] == "None":
        nodes -= 1
        indeces.append(i)
    i += 1

for i in indeces:
    j = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][i]["node_id"]:
            data["Sheet1"][i]["child_nodes"].append(node["node_id"])
            data["Sheet1"][i]["children"] += 1
            nodes -= 1
            jndeces.append(j)
        j += 1

indeces = []
for j in jndeces:
    i = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][j]["node_id"]:
            data["Sheet1"][j]["child_nodes"].append(node["node_id"])
            data["Sheet1"][j]["children"] += 1
            nodes -= 1
            indeces.append(i)
        i += 1

jndeces = []
for i in indeces:
    j = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][i]["node_id"]:
            data["Sheet1"][i]["child_nodes"].append(node["node_id"])
            data["Sheet1"][i]["children"] += 1
            nodes -= 1
            jndeces.append(j)
        j += 1

indeces = []
for j in jndeces:
    i = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][j]["node_id"]:
            data["Sheet1"][j]["child_nodes"].append(node["node_id"])
            data["Sheet1"][j]["children"] += 1
            nodes -= 1
            indeces.append(i)
        i += 1

jndeces = []
for i in indeces:
    j = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][i]["node_id"]:
            data["Sheet1"][i]["child_nodes"].append(node["node_id"])
            data["Sheet1"][i]["children"] += 1
            nodes -= 1
            jndeces.append(j)
        j += 1

indeces = []
for j in jndeces:
    i = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][j]["node_id"]:
            data["Sheet1"][j]["child_nodes"].append(node["node_id"])
            data["Sheet1"][j]["children"] += 1
            nodes -= 1
            indeces.append(i)
        i += 1

jndeces = []
for i in indeces:
    j = 0
    for node in data["Sheet1"]:
        if node["parent_node_id"] == data["Sheet1"][i]["node_id"]:
            data["Sheet1"][i]["child_nodes"].append(node["node_id"])
            data["Sheet1"][i]["children"] += 1
            nodes -= 1
            jndeces.append(j)
        j += 1

with open('node_data_out.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
json_file.close()

print(nodes)
