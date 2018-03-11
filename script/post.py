#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests

url = "http://192.168.0.161"
port = 80
headers = {'Content-Type': 'application/json'}


def get_account_info(device_id,lat,lon):
    id = "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"
    api_url = '{0}:{2}/checkfence/{1}'.format(url,id,port)
    print(api_url)
    params= {'lat':lat,'lon':lon}
    params = json.dumps(params).encode('utf8')
    response = requests.post(api_url,data=params, headers=headers)
    print(response)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

print(get_account_info(1,39.78,-6.3))