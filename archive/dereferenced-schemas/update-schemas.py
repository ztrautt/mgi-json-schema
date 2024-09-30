#!/usr/bin/env python

import getpass
import requests
import sys
import json
import glob

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_response(r,quiet=False):
    try:
        r_content = r.json()
    except:
        r_content = r.text
    if str(r.status_code)[0] is not '2':
        if not quiet: print('Error: ',r.status_code)
        if not quiet: print(r.text)
        sys.exit(0)
    else:
        return r_content

base_url = input('Enter cordra base url: ').strip('/')
user = input('Enter admin username: ')
pswd = getpass.getpass()

schemas = glob.glob('*.json')

for schema_file_name in schemas:
    schema_name = schema_file_name.replace('.json','')
    js_name = schema_file_name.replace('.json','.js')
    with open(schema_file_name) as f:
        schema_data = json.load(f)
    
    with open(js_name) as f:
        JS_data = f.read()
    
    schema = dict()
    schema['name'] = schema_name
    schema['schema'] = schema_data
    schema['javascript'] = JS_data
    
    url = base_url + '/objects/?query=type%3ASchema%20AND%20/name%3A' + schema_name
    
    try:
        r = requests.get(url, auth=(user, pswd), verify=False)
        result = check_response(r)
        schema_id = result['results'][0]['id']
    except Exception as e:
        print(e)
    
    url = base_url + '/objects/' + schema_id
    print(url)
    
    try:
        r = requests.put(url, data=json.dumps(schema), auth=(user, pswd), verify=False)
        print(check_response(r))
    except Exception as e:
        print(e)