import requests
import json

token_file = 'token.json'
creds_file = 'creds.json'


def getUser():
    # Aruba Central - Access + Refresh Tokens
    print("\nImporting Tokens...")
    token_json = readJSON(token_file)
    try:
        access_token = token_json['access_token']
        refresh_token = token_json['refresh_token']
    except KeyError as error:
        print("ERROR -> Missing key/value pair in", token_file, "->", error)
        exit()
    print("SUCCESS")

    # Aruba Central - Base URL + Account Credentials + Client ID/Secret
    print("\nImporting Credentials...")
    creds_json = readJSON(creds_file)
    try:
        base_url = creds_json['base_url']
        customer_id = creds_json['customer_id']
        username = creds_json['username']
        password = creds_json['password']
        client_id = creds_json['client_id']
        client_secret = creds_json['client_secret']
    except KeyError as error:
        print("ERROR -> Missing key/value pair in", creds_file, "->", error)
        exit()
    print("SUCCESS")

    print("\nCustomer ID: {0}\nUsername: {1}\nBase URL: {2}\nClient ID: {3}\nClient Secret: {4}\nAccess Token: {5}\nRefresh Token: {6}"
          .format(customer_id, username, base_url, client_id, client_secret, access_token, refresh_token))

    print("\nVerifying Access Token...")
    api_response = testAccessToken(base_url, access_token)
    if 'error' in api_response:
        print("ERROR -> Invalid Access Token:", api_response['error'], "->", api_response['error_description'])

        print("\nRefreshing access token using refresh token...")
        token_response = refreshToken(base_url, client_id, client_secret, refresh_token)
        if 'error' in token_response:
            print("ERROR -> Invalid Refresh Token:", token_response['error'], "->", token_response['error_description'])

            print("\nAuthenticating to Aruba Central...")
            login_response = authenticateCentral(base_url, client_id, username, password)
            if login_response.status_code == 200:
                csrf = login_response.cookies['csrftoken']
                sess = "session=" + login_response.cookies['session']
                print("CSRF Cookie:", csrf, "\nSession Cookie:", sess)

                print("\nRequesting authorization code...")
                auth_response = authorizeCentral(base_url, client_id, customer_id, csrf, sess)
                if 'auth_code' in auth_response:
                    auth_code = auth_response['auth_code']
                    print("Authorization Code:", auth_code)

                    print("\nExchanging for access and refresh token...")
                    token_response = obtainToken(base_url, client_id, client_secret, auth_code)
                    if not 'error' in token_response:
                        access_token = token_response['access_token']
                        refresh_token = token_response['refresh_token']
                        writeJSON('token.json', token_response)
                        print("Access Token:", access_token, "\nRefresh Token:", refresh_token)
                    else:
                        print("ERROR -> Cannot retrieve access token:", token_response['error'], "->",
                              token_response['error_description'])
                        exit()
                else:
                    print("ERROR -> Cannot authorize to Aruba Central:", auth_response['message'])
                    exit()
            else:
                print("ERROR -> Cannot authenticate to Aruba Central: Status Code", login_response.status_code)
                exit()
        else:
            access_token = token_response['access_token']
            refresh_token = token_response['refresh_token']
            writeJSON('token.json', token_response)
            print("Access Token:", access_token, "\nRefresh Token:", refresh_token)
    else:
        print("SUCCESS")
    print("\n---------- *** ----------\n")
    return {
        "base_url": base_url,
        "access_token": access_token
    }


def authenticateCentral(base_url, client_id, username, password):
    url = base_url + '/oauth2/authorize/central/api/login'
    params = {"client_id":client_id}
    payload = {"username":username, "password":password}
    headers = {'Content-type':'application/json'}
    response = requests.post(url, params=params, data=json.dumps(payload), headers=headers)
    return response

def authorizeCentral(base_url, client_id, customer_id, csrf, sess):
    url = base_url + '/oauth2/authorize/central/api'
    params = {"client_id":client_id, "response_type":"code", "scope":"all"}
    payload = {"customer_id":customer_id}
    headers = {'Content-type':'application/json', 'X-CSRF-TOKEN':csrf, 'Cookie':sess}
    response = requests.post(url, params=params, data=json.dumps(payload), headers=headers)
    return response.json()

def obtainToken(base_url, client_id, client_secret, auth_code):
    url = base_url + '/oauth2/token'
    payload = {'client_id':client_id, 'client_secret':client_secret, 'grant_type':'authorization_code', 'code':auth_code}
    response = requests.post(url, data=payload)
    return response.json()

def refreshToken(base_url, client_id, client_secret, refresh_token):
    url = base_url + '/oauth2/token'
    payload = {'client_id':client_id, 'client_secret':client_secret, 'grant_type':'refresh_token', 'refresh_token':refresh_token}
    response = requests.post(url, data=payload)
    return response.json()

def testAccessToken(base_url, access_token):
    user = {
        "base_url": base_url,
        "access_token": access_token
    }
    return genericQuery(user, "/monitoring/v1/networks")

def genericQuery(user, request_path):
    url = user['base_url'] + request_path
    payload = {'access_token': user['access_token']}
    response = requests.get(url, params=payload)
    return response.json()

def readJSON(file_name):
    try:
        with open(file_name) as file_data:
            return json.load(file_data)
    except IOError as file_error:
        print("ERROR ->", file_name, "->", file_error)
        exit()

def writeJSON(file_name, file_data):
    try:
        with open(file_name, 'w') as outfile:
            return json.dump(file_data, outfile, indent=2)
    except IOError as file_error:
        print("ERROR ->", file_name, "->", file_error)
        exit()
