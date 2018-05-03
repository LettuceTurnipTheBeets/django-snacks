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

    return render(
        request,
        'index.html', {
            'snacks_always_purchased': snacks_always_purchased,
        }
    )
    
def suggestions(request):
    snacks = get_snacks()
    print(snacks)

    snack_options = []
    for item in snacks:
        if item['optional']:
            snack_options.append(item['name'])
    
    return render(
        request,
        'suggestions.html', {
            'snack_options': snack_options,
        }
    )

def suggest_snack(request):
    if request.method == 'POST':
        snack_option = request.POST.get('snackOptions')
        suggestion_input = request.POST.get('suggestionInput')
        suggestion_location = request.POST.get('suggestionLocation')

        message = 'Your snack was suggested!'

        print('option: {}\ninput: {}\nlocation: {}'.format(snack_option, suggestion_input, suggestion_location))

        if snack_option is None and suggestion_input == '' and suggestion_location == '':
            message = 'Please make a selection'
        elif suggestion_input == '' and suggestion_location == '':
            message = 'Record current optional suggestion'
        elif suggestion_input == '' and not suggestion_location == '':
            message = 'Please enter a snack name'
        elif not suggestion_input == '' and suggestion_location == '':
            message = 'Please enter a snack location'

        print(message)

 
