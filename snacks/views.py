from django.http import HttpResponse
from django.shortcuts import render
from snacks.services import get_snacks
import requests


def voting(request):
    snacks = get_snacks()
    print(snacks)

    snacks_always_purchased = []
    for item in snacks:
        if not item['optional']:
            snacks_always_purchased.append(item['name'])

    #return HttpResponse("Hello, world. You're at the voting page.")
    return render(
        request,
        'index.html', {
            'snacks_always_purchased': snacks_always_purchased,
        }
    )
    
def suggestions(request):
    #return HttpResponse("Hello, world. You're at the suggestions page.")
    return render(
        request,
        'suggestions.html'
    )
