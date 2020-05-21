import flask
from ratelimit import limits
from flask import request
from db_connect import DatabaseConnector
import hashlib

app = flask.Flask(__name__)
app.config["DEBUG"] = True

FIFTEEN = 900


@limits(calls=30, period=FIFTEEN)
@app.route('/', methods=['GET'])
def home():
    return ""


@app.errorhandler(400)
def bad_request(e):
    return "Error 400: Incorrect Parameters"


@app.errorhandler(403)
def access_denied(e):
    return "Error 403: Access Denied"


@app.errorhandler(404)
def file_not_found(e):
    return "Error 404: Resource Not Found"


@limits(calls=30, period=FIFTEEN)
@app.route('/api/v1/resources/measurements', methods=['GET'])
def api_search_one():
    params = request.args
    id = params.get('id')
    year = params.get('year')
    month = params.get('month')
    day = params.get('day')
    date = year + "-" + month + "-" + day

    if not (id and year and month and day):
        return bad_request(400)

    db_client = DatabaseConnector("mongodb://localhost:27017", "Measurements", str(id))
    query = {"Time": date}
    response = db_client.find_one(query)

    if not response:
        return file_not_found(404)
    else:
        print(response)
        return response


@limits(calls=618, period=FIFTEEN)
@app.route('/api/v1/resources/measurements', methods=['POST'])
def api_search_range():
    body = request.get_json()

    id = body['id']
    d1 = body['from'].strptime("%Y-%m-%d")
    d2 = body['to'].strptime("%Y-%m-%d")
    username = body['username']
    password = body['password']

    if not (id or d1 or d2):
        return bad_request(400)

    user_client = DatabaseConnector("mongodb://localhost:27017", "Users", "Users")
    query = {"Username": username, "Password": hashlib.sha256(password)}
    if not user_client.exists(query):
        return access_denied(403)

    db_client = DatabaseConnector("mongodb://localhost:27017", "Measurements", str(id))
    query = {"Date": {"$gte": d1, "$lt": d2}}
    response = db_client.find(query)

    if not response:
        return file_not_found(404)
    else:
        print(response)
        return response


@limits(calls=5, period=FIFTEEN)
@app.route('/api/v1/resources/users', methods=['POST'])
def new_user():
    body = request.get_json()
    username = body['username']
    password = body['password']
    db_client = DatabaseConnector("mongodb://localhost:27017", "Users", "Users")
    query = {"Username": username}
    if db_client.exists(query):
        return bad_request(400)
    else:
        passhash = hashlib.sha256(password)
        record = {"Username": username, "Password": passhash}
        db_client.insert_record(record)


app.run()
