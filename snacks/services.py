import requests
from settings_secret import api_key
url = 'https://api-snacks.nerderylabs.com/v1/snacks/?ApiKey=' + api_key


def get_snacks():
    params = {}
    r = requests.get(url, params=params)
    snacks = r.json()
    
    return snacks


def post_snacks(name, location, latitude, longitude):
    data = {'name': name, 'location': location, 'latitude': latitude, 'longitude': longitude}
    headers = {'User-Agent': 'Mozilla/5.0'}
    requests.post(url, data=params, headers=headers)
