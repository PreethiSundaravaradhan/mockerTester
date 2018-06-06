import json
import sys
import requests
import requests.auth

# import flask
# from flask import Flask, request, redirect, session, url_for
# from flask.json import jsonify
from oauthlib.oauth2 import BackendApplicationClient
from from_official import mongo_add, get_mongo_users

token = ''
sys.path.append('/usr/local/var/pyenv/versions/2.7.12/lib/python2.7/site-packages/')

def mongo_add_person(name):
    person = {'name': name,'age':1,'status': 'pending'}
    mongo_add(person)
    usr = get_mongo_users()
    cursor = usr.find({"age": {"$exists": True}})
    for document in cursor:
        if(usr['age'] != None):
            usr.update(document, {'$set' : {'age' : document['age'] + 1}})
    return usr

def box_oauth():
    #auth_url, csrf_token = oauth.get_authorization_url('https://account.box.com/requests.api/oauth2/authorize')

    scope = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile']
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                               scope=scope)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://provider.com/oauth2/token', client_id=client_id,
                              client_secret=client_secret)
    return

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
    es = json.loads(response.text)
    if(es['hits']['total'] == 0):
        return None
    return es['hits']['hits']


def func_sample():
    box_get_file_uri = 'https://api.box.com/2.0/files/295640148418'
    box_token = '6h94VXU5AzyJUlA2P3mNqY5bFS2EmlhU'
    #box_token = box_oauth2

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

# This information is obtained upon registration of a new box
def box_oauth2():
    client_id = 'mwharq3zelv02ye2a6vhevhs98sx9z8k'
    client_secret = 'OONtZLMnzBXk6sW5hg2xa6iYgZvRaWLT'
    redirect_uri = 'https://app.box.com'
    authorization_base_url = 'https://api.box.com/oauth2/authorize'
    token_url = 'https://api.box.com/oauth2/token'
    box_client = OAuth2Session(client_id)
    authorization_url, state = box_client.authorization_url(authorization_base_url)
    print 'Please go here and authorize,', authorization_url
    redirect_response = raw_input('Paste the full redirect URL here:')
    t = box_client.fetch_token(token_url, client_secret=client_secret,authorization_response = redirect_response)
    print("token=="+t)
    return t

# @app.route("/login")
# def login():
#     github = OAuth2Session(client_id)
#     authorization_url, state = github.authorization_url(authorization_base_url)
#
#     # State is used to prevent CSRF, keep this for later.
#     session['oauth_state'] = state
#     return redirect(authorization_url)
#
# @app.route("/callback")
# def callback():
#     github = OAuth2Session(client_id, state=session['oauth_state'])
#     token = github.fetch_token(token_url, client_secret=client_secret,
#                                authorization_response=request.url)
#
#     return jsonify(github.get('https://api.github.com/user').json())
func_sample()