import requests
from settings_secret import url, api_key
url = url + api_key


def get_snacks():
    params = {}
    
    try:
        r = requests.get(url, params=params)
        snacks = r.json()
    except requests.exceptions.RequestException:
        snacks = 'API Error'
    
    return snacks


def post_snacks(name, location):
    data = {'name': name, 'location': location}
    
    try:
        output = requests.post(url, data=data)
    except requests.exceptions.RequestException:
        output = 'API Error'

    return output
