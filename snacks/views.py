from django.http import HttpResponse
from django.shortcuts import render
import requests


def voting(request):
    url = 'https://api-snacks.nerderylabs.com/v1/snacks/?ApiKey=ff5d8fd9-80ec-40c3-8eed-87dfc966e1bc'
    params = {}
    r = requests.get(url, params=params)
    snacks = r.json()
    print(snacks)

    #return HttpResponse("Hello, world. You're at the voting page.")
    return render(
        request,
        'index.html',
    )
    
def suggestions(request):
    #return HttpResponse("Hello, world. You're at the suggestions page.")
    return render(
        request,
        'suggestions.html'
    )
