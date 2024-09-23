import requests


def get_refresh_token(code, client_id, client_secret):
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    response_json = response.json()
    try:
        refresh_token = response_json['refresh_token']
    except KeyError:
        print(f"A problem occurred: {response_json} \nmost likely the code is invalid.")
        raise Exception("Invalid code")
    
    return refresh_token, response_json['athlete']['id']



def get_access_token(refresh_token, client_id, client_secret):
    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token"
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    try:
        access_token = res.json()['access_token']
    except:
        print(res.json())
        return None

    print("Access Token = {}\n".format(access_token))

    return access_token
