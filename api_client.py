import datetime
import http.client
import json
import hashlib
import urllib


def _get_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


class APIClient(object):

    def __init__(self, protocol, host, port, api_key, secret):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.api_key = api_key
        self.secret = secret

    def _get_signature(self, json_dump, timestamp):
        to_be_signed = 'json=%s&api_key=%s&timestamp=%s&secret=%s' % (json_dump, self.api_key, timestamp, self.secret)
        to_be_signed_encoded = to_be_signed.encode()
        return hashlib.sha256(to_be_signed_encoded).hexdigest()

    def _get_connection(self):
        if self.protocol == 'http':
            return http.client.HTTPConnection(self.host, self.port)
        elif self.protocol == 'https':
            return http.client.HTTPSConnection(self.host, self.port)

    def _make_request(self, url, query):
        json_dump = json.dumps(query)
        timestamp = _get_timestamp()
        signature = self._get_signature(json_dump, timestamp)

        request_data = urllib.parse.urlencode(
            {'json': json_dump, 'api_key': self.api_key, 'timestamp': timestamp, 'signature': signature})

        connection = self._get_connection()
        connection.request('POST', url, request_data)
        response = connection.getresponse()
        print(response.status)
        response_data = response.read()
        connection.close()

        return json.loads(response_data)

    def query_datalogs(self, query):
        return self._make_request('/api/third-party/datalogs/query/', query)
