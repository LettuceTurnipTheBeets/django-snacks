import requests
from settings_secret import url, api_key
url = url + api_key


def get_snacks():
    params = {}
    r = requests.get(url, params=params)
    snacks = r.json()
    
    return snacks


def post_snacks(name, location):
    data = {'name': name, 'location': location}
    #headers = {'User-Agent': 'Mozilla/5.0'}
    
    output = requests.post(url, data=data)
    print(output)
