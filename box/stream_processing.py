#!/usr/local/var/pyenv/shims/python

import json
import time

import requests

def write_event_to_file(uri, header, stream_position, etype=None):
    params = {'stream_position': stream_position, 'event_type': etype}
    response = requests.get(uri, headers=header, params=params)
    file_meta = json.loads(response.text)
    print(json.dumps(file_meta, indent=2))
    with open('../tests/data/events/get_many2.json', 'a') as events_file:
        events_file.write(json.dumps(file_meta, indent=2, encoding='UTF-8'))
    return file_meta['next_stream_position']


def get_event(uri, header, stream_position, etype=None):
    params = {'stream_position': stream_position, 'event_type': etype}
    response = requests.get(uri, headers=header, params=params)
    file_meta = json.loads(response.text)
    print(json.dumps(file_meta, indent=2))
    with open('../tests/data/events/get_many_'+str(time.time())+'.json', 'a') as events_file:
        events_file.write(json.dumps(file_meta, indent=2, encoding='UTF-8'))
    return file_meta


def get_first_event(token, chunk=10, e_type=None):
    uri = 'https://api.box.com/2.0/events'
    header = {'Authorization': 'Bearer ' + token}
    print("##### etype"+e_type)
    params = {'limit': chunk, 'event_type': e_type}
    response = requests.get(uri, headers=header, params=params)
    file_meta = json.loads(response.text)
    stream_pos = file_meta['next_stream_position']
    for itr in range(95):
        events = get_event(uri, header, stream_pos, e_type)
        stream_pos = events['next_stream_position']
    return


if __name__ == '__main__':
    token = 'NYgUySDETcKEF77NBcJW3i8Ba9ftkshz'
    get_first_event(token, 100, 'ITEM_TRASH')
