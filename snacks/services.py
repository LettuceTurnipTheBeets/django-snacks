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
    """Return the total seconds between now and the end of the month.
    This is used to set the cookie expiration date.  It is assumed that
    each month cycle is reset on the 1st of the month.
    """ 
    now = datetime.utcnow() - timedelta(hours=5)

    if now.month == 12:
        next_month = datetime(now.year + 1, 1, 1)
    else:
        next_month = datetime(now.year, now.month + 1, 1)

    return (next_month - now).seconds
