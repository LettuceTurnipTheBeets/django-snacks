from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from snacks.services import get_snacks
from snacks.models import Snack
import requests


def voting(request):
    snacks = get_snacks()

    snacks_always_purchased = []
    snacks_suggested = []
    snack_date = []
    snack_total_votes = []
    snack_voted_for = []
    error_message = ''

    if snacks == 'API Error':
        api_error = True
        votes_remaining = 'NA'
        out_of_votes = False
        create_cookie = False
    else:
        api_error = False
        for item in snacks:
            if not item['optional']:
                snacks_always_purchased.append(item['name'])
            elif item['optional']:
                snacks_suggested.append([item['name']])
            
                if item['lastPurchaseDate'] == 'null':
                    snack_date.append('')
                else:
                    snack_date.append(item['lastPurchaseDate'])

                try:
                    snack_total_votes.append(Snack.objects.get(name=item['name']).votes)
                except Snack.DoesNotExist:
                    snack_total_votes.append(Snack.objects.create(name=item['name'], votes=0).votes)

        if 'votes_remaining' in request.COOKIES:
            create_cookie = False

            if int(request.COOKIES['votes_remaining']) < 0:
                out_of_votes = True
                votes_remaining = 0
            else:
                out_of_votes = False
                votes_remaining = int(request.COOKIES['votes_remaining'])

        else:
            create_cookie = True
            votes_remaining = 3

        for index, snack in enumerate(snacks_suggested):
            snack.append(snack_total_votes[index])
            snack.append(snack_voted_for[index])
            snack.append(snack_date[index])       

    response = render(
        request,
        'index.html', {
            'snacks_always_purchased': snacks_always_purchased,
            'snacks_suggested': snacks_suggested,
            'votes_remaining': votes_remaining,
            'out_of_votes': out_of_votes,
            'api_error': api_error,
        }
    )

    if create_cookie:
        response.set_cookie(key='votes_remaining', value=3)
    if out_of_votes:
        response.set_cookie(key='votes_remaining', value=0)

    return response

def vote(request, name):
    if request.method == 'POST':
        print(name)

        votes_remaining = int(request.COOKIES['votes_remaining']) - 1        
        
        if votes_remaining >= 0:
            snack = Snack.objects.get(name=name)
            print(snack.votes)
            snack.votes = snack.votes + 1
            snack.save()
            print(snack.votes)
    
    response = HttpResponseRedirect('/voting/')
    
    response.set_cookie('votes_remaining', votes_remaining)
    return response    

def suggestions(request):
    snacks = get_snacks()
    error_code = 0
    out_of_suggestions = False

    if snacks == 'API Error':
        error_code = -4
        snack_options = []
        create_cookie = False
    else:     
        if 'suggestions_remaining' in request.COOKIES:
            print('suggestions remaining: {}'.format(request.COOKIES['suggestions_remaining']))
            create_cookie = False

            if int(request.COOKIES['suggestions_remaining']) == -1:
                error_code = int(request.COOKIES['suggestions_remaining']) 
                out_of_suggestions = True
            elif int(request.COOKIES['suggestions_remaining']) < -1:
                error_code = int(request.COOKIES['suggestions_remaining'])
                create_cookie = True
            else:
                error_code = 0
        else:
            create_cookie = True

        snack_options = []
        for item in snacks:
            if item['optional']:
                snack_options.append(item['name'])
   
    print("error code: {}".format(error_code)) 
    response = render(
        request,
        'suggestions.html', {
            'snack_options': snack_options,
            'error_code': error_code,
        }
    )

    if create_cookie:
        response.set_cookie(key='suggestions_remaining', value=1)
    if out_of_suggestions:
        response.set_cookie(key='suggestions_remaining', value=0)

    return response

def suggest_snack(request):
    if request.method == 'POST':
        snack_option = request.POST.get('snackOptions')
        suggestion_input = request.POST.get('suggestionInput')
        suggestion_location = request.POST.get('suggestionLocation')
        error_code = 1
        
        if int(request.COOKIES['suggestions_remaining']) == 0:
            error_code = -1
        elif not suggestion_input == '' and not suggestion_location == '':
            snacks = get_snacks()
        
            for item in snacks:
                if item['optional']:
                    if suggestion_input == item['name']:
                        error_code = -2
                        break
        elif (snack_option is None and suggestion_input == '' and suggestion_location == '') or (suggestion_input == '' and not suggestion_location == '') or (not suggestion_input == '' and suggestion_location == ''):
            error_code = -3

    response = HttpResponseRedirect('/suggestions/')

    if error_code == 1:
        response.set_cookie('suggestions_remaining', 0)
    else:
        response.set_cookie('suggestions_remaining', error_code)
    
    return response
 

