import requests
import subprocess
from datetime import datetime  
from datetime import timedelta  
from settings_secret import url, api_key
url = url + api_key


def get_snacks():
    """Return the output of a GET request to the API.  
    If successful it returns a dictionary of the json response.
    If unsuccessful, it returns 'API Error'.
    """

    params = {}

    try:
        r = requests.get(url, params=params)
        snacks = r.json()
    except requests.exceptions.RequestException:
        snacks = 'API Error'

    return snacks


def post_snacks(name, location):
    """Return the output of a POST request to the API.
    Takes in the 'name' and 'location' arguments which are required in a POST
    request.  If successful, it returns a dictionary of the json response.
    If unsuccessful, it returns 'API Error'.
    """
    bash_command_split = [
        'http',
        'POST',
        url,
        'name=' + name,
        'location=' + location,
    ]
    process = subprocess.Popen(bash_command_split, stdout=subprocess.PIPE)
    output = process.communicate()

    return output

def get_expiry_time():

