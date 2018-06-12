#!/usr/local/var/pyenv/shims/python
import json
import sys
import requests
import requests.auth
from box_apis import box_api
from from_official import mongo_add, get_mongo_users


def mongo_add_person(name):
    person = {'name': name,'age':1,'status': 'pending'}
    x = mongo_add(person)
    usr = get_mongo_users()
    print("mongo after adding -->"+str(x))
    cursor = usr.find({"age": {"$exists": True}})
    for document in cursor:
        if(usr['age'] != None):
            usr.update(document, {'$set' : {'age' : document['age'] + 1}})
    return usr

def mongo_add_json(data):
    x = mongo_add(data)
    #usr = get_mongo_users()
    return x

def es_get_person(name):
    es_loc = 'http://localhost:9200/accounts/person/_search?q='+name
    response = requests.get(es_loc)
    print("\nelastic search true call -->")
    es = json.loads(response._content)
    print(es)
    if(es['hits']['total'] == 0):
        return None
    return es['hits']['hits']


def collab_files_on_folder(token, parent_0, user_q):

    box = box_api(token)

    # box create folder/subfolders and some random files
    folder_id = box._folder_create("somefolder8", parent_0)
    box._file_upload(folder_id, "textfile.txt")
    uploaded_f_id3 = box._folder_create("somefolder2_l3", folder_id)

    # get all subfolder in parent
    all_folders = box._get_folder_entries(folder_id)

    # get collab for uploaded_f_id3
    # add to mongo
    collabfid3 = box._collab_one_file(uploaded_f_id3)
    parent_collab = box._collab_one_file(folder_id)
    mongo_add(collabfid3)

    for entry in collabfid3['entries']:
        if entry['accessible_by']['login'] == user_q:
            user_id = entry['accessible_by']['id']
            del_status = box._remove_collab(entry['id'])
            print("delete status == "+str(del_status))

    all_folders_ad = box._get_folder_entries(folder_id)
    new_parent_collab = box._collab_one_file(folder_id)
    count = 0
    for entry in all_folders:
        for collab_old in parent_collab["entries"]:
            found = 0
            for collab_new in new_parent_collab["entries"]:
                if(collab_old['accessible_by']['login'] == collab_new['accessible_by']['login']):
                    found = 1
            if found == 0:
                ++count
                box._collab_post(entry["item"]["id"], user_id)

    mongo_add_person(user_q)

    # some mongo call
    mongo_add_person(parent_collab["entries"][0]['accessible_by']['name'])

    # es call
    es_person = es_get_person(user_q)

    print('\nother logic true responses --> ')
    # 'other calls'
    if (es_person is None):
        print('none')
    else:
        print(es_person)

    return count

def func_sample():
    box_get_file_uri = 'https://api.box.com/2.0/files/285571189078'
    box_dev_token = 'VdU3PWHbKXfx4r3AOvX2mcwrGXAOJZsx'
    #box_token = box_oauth2()

    box = box_api(box_dev_token)
    #box call
    box_file_owner = box._get_one_file('295987792281')

    ##some mongo call
    p_name = box_file_owner
    #print(p_name)
    mongo_add_person(p_name)

    #es call
    es_person = es_get_person(box_file_owner)

    print('\nother logic true responses --> ')
    #'other calls'
    if(es_person is None):
        print('none')
    else:
        print(es_person)

    return

if __name__ == "__main__":
    token = '1kZcBmbGgWDMk4u1sEyagBDe0LBFpaow'
    parent_0 = '50218147730'
    user_q = 'Preethi_Sundaravarad@symantec.com'
    collab_files_on_folder(token, parent_0, user_q)

dicti = []