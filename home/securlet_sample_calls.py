import json
import random

import requests

from from_official import mongo_add, get_mongo_users


def mongo_add_person(name):
    person = {'name': name,'age':1,'status': 'pending'}
    mongo_add(person)
    usr = get_mongo_users()
    cursor = usr.find({"age": {"$exists": True}})
    for document in cursor:
        if(usr['age'] != None):
            usr.update(document, {'$set' : {'age' : document['age'] + 1}})
    return usr

def box_get_api(uri, authtoken):
    response = requests.get(
        uri, headers={'Authorization': 'Bearer '+authtoken})
    file_meta = json.loads(response.text)
    owner = file_meta['owned_by']['name']
    print("response ==" +response.text)
    return owner

def es_get_person(name):
    es_loc = 'http://localhost:9200/accounts/person/_search?q='+name
    response = requests.get(es_loc)
    print(response.text)
    es = json.loads(response.text)
    if(es['hits']['total'] == 0):
        return None
    return es['hits']['hits']


def func_sample():
    box_get_file_uri = 'https://api.box.com/2.0/files/295640148418'
    box_token = 'brVrvOGZX7wT2fKb3zOfYNeusejWx5Zy'

    #box call
    box_file_owner = box_get_api(box_get_file_uri, box_token)

    ##some mongo call
    p_name = box_file_owner
    #print(p_name)
    mongo_add_person(p_name)

    #es call
    es_person = es_get_person(box_file_owner)

    #'other calls'
    if(es_person is None):
        print('none')
    else:
        print(es_person)

    return


func_sample()