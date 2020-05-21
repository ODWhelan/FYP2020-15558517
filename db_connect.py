import pymongo
from bson.json_util import dumps


class DatabaseConnector(object):

    def __init__(self, url, db_name, collection_name):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[db_name]
        self.col = self.db[collection_name]

    def insert_record(self, record):
        x = self.col.insert_one(record)
        return x

    def insert_many_records(self, records):
        x = self.col.insert_many(records)
        return x

    def exists(self, query):
        res = self.col.find_one(query)
        if res:
            return True
        else:
            return False

    def update_record(self, query, record):
        x = self.col.update(query, record)
        return x

    def find_one(self, query):
        return dumps(self.col.find_one(query))

    def find(self, query):
        return dumps(self.col.find(query))
