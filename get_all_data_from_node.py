from api_client import APIClient
from db_connect import DatabaseConnector
import datetime
import json


def generate_query(client, num, today):
    day = today
    null = 0
    while True:
        day_after = day
        day = day - datetime.timedelta(days=1)
        query = [{
            'request_id': 'Request ID',
            'node_id': '%d' % num,
            'request_type': 'usage',
            'from_date': day.strftime("%Y-%m-%d"),
            'to_date': day_after.strftime("%Y-%m-%d"),
            'group': 'raw',
            'timezone': 'UTC',
            'date_format': 'iso',
            'ignore_today': False
        }]
        response = client.query_datalogs(query)
        if "results" in response.keys():
            values = [x['value'] for x in response['results'][0]['datapoints']]
            db_client = DatabaseConnector("mongodb://localhost:27017", "Measurements", str(num))
            record = {"Time": day.strftime("%Y-%m-%d"), "Date": day, "Value:": response['results'][0]['datapoints']}
            db_client.insert_record(record)

            # Check if the array is empty
            if values.count(None) < len(values):
                null = 0
            elif null < 5:
                print("null")
                null += 1
            # If five arrays in a row are empty, it's probably the end
            else:
                leaves = DatabaseConnector("mongodb://localhost:27017", "Meta", "End Nodes")
                query = {"node_id": str(num)}
                meta = json.loads(leaves.find_one(query))
                meta['earliest_data'] = day.strftime("%Y-%m-%d")
                print(meta)
                meta.pop("_id")
                leaves.update_record(query, meta)
                return
        # Reached the last accepted date
        else:
            leaves = DatabaseConnector("mongodb://localhost:27017", "Meta", "End Nodes")
            query = {"node_id": str(num)}
            meta = json.loads(leaves.find_one(query))
            meta['earliest_data'] = day.strftime("%Y-%m-%d")
            print(meta)
            meta.pop("_id")
            leaves.update_record(query, meta)
            return


def main():
    today = datetime.datetime.now()
    client = APIClient('https', 'cylonaem.com', 443, 'ucd-api', 'xolg-cpgo-ugzc-itve-zbdj-sjgp-tdtn-ydad')
    fin = open("nodes.txt", "r")
    for num in fin:
        node = int(num)
        print(node)
        generate_query(client, node, today)
    fin.close()


if __name__ == "__main__":
    main()
