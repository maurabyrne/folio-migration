#!/usr/local/bin/python3.6

# This script is trying to do 6 things.
#    1. Connect to the login URL and get the X-Okapi-Token  --> DONE.
#    2. Download all of the permissions that exist on the server.  --> DONE.
#    3. Take every permission that ends in ".all" and write it to a file called
#         "folio-admin"  --> DONE.
#    4. Upload the "folio-admin" permissions using the name "Folio Admin"
#    5. Take every permission that ends in ".get" and write it to a file called
#         "view-all"
#    6. Get list of restricted view permissions and pull them out of "view-all"
#    7. In future, loop through the list of permissions and
#       a. Organize them by module and function
#       b. Compare them to permissons sets already established
#       c. Identify new permissions, especially non-standard names and new
#          modules.
#       d. Upload new permissions sets using .get, .all, and middle set of
#          .post and .put for specific modules and functions.

from pprint import pprint
import requests
import json
import os


CONFIG = {
    #EBSCO tenant settings
    # These settings are kept offline
    #'okapi_base_url': 'Ebsco_url',
    #'username': 'username',
    #'password': 'password',
    #'tenant': 'tenant'
    #
    #Local tenants
    # These also have placeholders for settings
    #'okapi_base_url': 'local_tenant_1',
    #'okapi_base_url': 'local_tenant_2',
    #'okapi_base_url': 'local_tenant_3',
    #'username': 'local_username',
    #'password': 'local_password',
    #'tenant': 'local_tenant'
    #
    # FOLIO project tenant settings
    # Placeholders
    #'okapi_base_url': 'placeholder_url',
    #'username': 'placholder_username',
    #'password': 'placeholder_password',
    #'tenant': 'placeholder_tenant',
    }

def get_auth_token():
    global CONFIG
    tenant = CONFIG['tenant']
    username = CONFIG['username']
    password = CONFIG['password']
    url = CONFIG['okapi_base_url'] + '/authn/login'
    headers = {"Content-type": "application/json", "X-Okapi-Tenant": tenant}
    payload = {"username":username, "password":password}
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    return r.headers['x-okapi-token']

def get_permissions(token):
    global CONFIG
    tenant = CONFIG['tenant']
    url = CONFIG['okapi_base_url'] + '/perms/permissions?length=10000'
    headers = {"Content-type": "application/json", "X-Okapi-Tenant": tenant, "X-Okapi-Token": token}
    r = requests.get(url, headers=headers)
    d = r.json()
    perms = d['permissions']
    all_perms_list = [p['permissionName'] for p in perms]#['permissions']]

#    all_perms_list = [p['permissionName'] for p in perms if p['permissionName'][-4:] == '.all']
    view_all_list = [p['permissionName'] for p in perms if p['permissionName'][-4:] == '.get']
    return all_perms_list
#    return view_all_list

def upload_permissions(token):
    global CONFIG
    tenant = CONFIG['tenant']
    url = CONFIG['okapi_base_url'] + '/perms/permissions'
    headers = {"Content-type": "application/json", "X-Okapi-Tenant": tenant, "X-Okapi-Token": token}
    perms = get_permissions(token)
    payload = {"permissionName" : "all_perms_list", "displayName" : "Folio Admin", "mutable" : 'true', "visible" : 'true', "subPermissions" : perms}
    a = requests.post(url, headers=headers, data=json.dumps(payload))

token = get_auth_token()
upload_permissions(token)
