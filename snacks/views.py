from django.http import HttpResponseRedirect
from django.shortcuts import render
from snacks.services import get_snacks
from snacks.models import Snack
import requests


def voting(request):
    snacks = get_snacks()
    #print(snacks)

    snacks_always_purchased = []
    snacks_suggested = []
    suggested_date = []    
    votes = []

    for item in snacks:
        if not item['optional']:
            snacks_always_purchased.append(item['name'])
        elif item['optional']:
            snacks_suggested.append([item['name']])
            
            if item['lastPurchaseDate'] == 'null':
                 suggested_date.append('')
            else:
                suggested_date.append(item['lastPurchaseDate'])

            try:
                votes.append(Snack.objects.get(name=item['name']).votes)
            except Snack.DoesNotExist:
                votes.append(Snack.objects.create(name=name, votes=0).votes)

    print(snacks_suggested)
    for index, snack in enumerate(snacks_suggested):
        snack.append(votes[index])
        snack.append('icon-check_voted')
        snack.append(suggested_date[index])       
    print(snacks_suggested)


    return render(
        request,
        'index.html', {
            'snacks_always_purchased': snacks_always_purchased,
            'snacks_suggested': snacks_suggested,
        }
    )

def vote(request, name):
    if request.method == 'POST':
        print(name)
        
        snack = Snack.objects.get(name=name)
        print(snack.votes)
        snack.votes = snack.votes + 1
        snack.save()
        print(snack.votes)
    
    return HttpResponseRedirect('/voting/')
    
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
    
    return HttpResponseRedirect('/suggestions/')
 
