#!/usr/bin/env python

import config
import repositories
import requests
import json


url = config.datacite_test_host + "/dois"
username = config.datacite_test_user
password = config.datacite_test_pw
prefix = config.datacite_test_prefix
headers = {"Content-Type": "application/vnd.api+json"}

payload = {
    'data': {
        'attributes': {'prefix': '10.81057'},
        'type': 'dois'
    }
}

print(url)
print(username)
print(password)
print(prefix)
print(headers)
print(payload)
print()
r = requests.post(url, headers = headers, data = json.dumps(payload), auth = (username, password))
print(r.text)
