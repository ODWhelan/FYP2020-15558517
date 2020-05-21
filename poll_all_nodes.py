from api_client import APIClient
from db_connect import DatabaseConnector


def generate_query(client, num):
    import datetime
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    query = [{
        'request_id': 'Request ID',
        'node_id': '%d' % num,
        'request_type': 'usage',
        'from_date': today.strftime("%Y-%m-%d"),
        'to_date': tomorrow.strftime("%Y-%m-%d"),
        'group': 'raw',
        'timezone': 'UTC',
        'date_format': 'iso',
        'ignore_today': False
    }]

    response = client.query_datalogs(query)
    if "results" in response.keys():
        db_client = DatabaseConnector("mongodb://localhost:27017", "Measurements", str(num))
        query = {"Time": today.strftime("%Y-%m-%d")}
        # Check if an entry for today already exists
        if db_client.exists(query):
            print(1)
            query = {"Time:": today.strftime("%Y-%m-%d")}
            record = {"Value:": response['results'][0]['datapoints']}
            db_client.update_record(query, record)
        else:
            print(2)
            record = {"Time": today.strftime("%Y-%m-%d"), "Date": today, "Value:": response['results'][0]['datapoints']}
            db_client.insert_record(record)


def main():
    client = APIClient('https', 'cylonaem.com', 443, 'ucd-api', 'xolg-cpgo-ugzc-itve-zbdj-sjgp-tdtn-ydad')
    fin = open("nodes.txt", "r")
    numbers = []
    for num in fin:
        numbers.append(num)
    fin.close()
    while True:
        for num in numbers:
            node = int(num)
            print(node)
            generate_query(client, node)


if __name__ == "__main__":
    main()
