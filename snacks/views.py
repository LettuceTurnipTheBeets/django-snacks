from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from snacks.services import get_snacks, post_snacks
from snacks.models import Snack
import requests


def voting(request):
    """Show the always purchased snacks and the suggested snacks which can
    be voted on.

    /voting/.

    Once this function is called it polls the API and separates the snacks
    into always purchased snacks and suggested snacks.  The suggested snacks
    can be voted on if the user has at least 1 vote remaining.  If the API is
    down for maintenance or the user tries to vote for a suggested snack
    without any votes remaining, an error message is shown.

    On submit this does to the vote() function.
    """
    snacks = get_snacks()
    snacks_always_purchased = []
    snacks_suggested = []
    snack_date = []
    snack_total_votes = []
    snack_voted_for = []
    error_message = ''
    out_of_votes = False

    if snacks == 'API Error':
        api_error = True
        votes_remaining = ''
        create_cookie = False
    else:
        api_error = False

        if ('votes_remaining' in request.COOKIES and
                'voted_for' in request.COOKIES):
            create_cookie = False

            if int(request.COOKIES['votes_remaining']) < 0:
                out_of_votes = True
                votes_remaining = 0
            else:
                votes_remaining = int(request.COOKIES['votes_remaining'])
        else:
            create_cookie = True
            votes_remaining = 3

        for item in snacks:
            if not item['optional']:
                snacks_always_purchased.append(item['name'])
            elif item['optional']:
                snacks_suggested.append([item['name']])

                if item['lastPurchaseDate'] == 'null':
                    snack_date.append('')
                else:
                    snack_date.append(item['lastPurchaseDate'])

                if ('voted_for' in request.COOKIES and
                        item['name'] in str(request.COOKIES['voted_for'])):
                    snack_voted_for.append(True)
                else:
                    snack_voted_for.append(False)

                try:
                    votes = Snack.objects.get(name=item['name']).votes
                    snack_total_votes.append(votes)
                except Snack.DoesNotExist:
                    votes = Snack.objects.create(name=item['name'], votes=0)
                    snack_total_votes.append(votes.votes)

        if ('votes_remaining' in request.COOKIES and
                'voted_for' in request.COOKIES):
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
        response.set_cookie('votes_remaining', 3)
        response.set_cookie('voted_for', '')
    if out_of_votes:
        response.set_cookie('votes_remaining', 0)

    return response


def vote(request, name):
    """Update the vote count for a suggested snack.
    This is the endpoint when a user clicks to vote on a suggested snack.

    /voting/vote/'name'.

    name:
      This is the name of the suggested snack that was voted for.

    Once this function is called it subtracts a vote from the user's
    votes_remaining cookie and adds the suggested snack name to the user's
    voted_for cookie. 

    After the votes are suggested snacks are reconciled it calls the voting()
    function.
    """
    if request.method == 'POST':
        votes_remaining = int(request.COOKIES['votes_remaining']) - 1
        voted_for = str(request.COOKIES['voted_for'])

        if votes_remaining >= 0:
            snack = Snack.objects.get(name=name)
            snack.votes += 1
            snack.save()
            voted_for = voted_for + name + ' '

    response = HttpResponseRedirect('/voting/')
    response.set_cookie('votes_remaining', votes_remaining)
    response.set_cookie('voted_for', voted_for)

    return response


def suggestions(request):
    """Show the suggested snacks and an input form for suggesting new snacks.

    /suggestions/.

    Once this function is called it polls the API to show a list of suggested
    snacks that haven't been suggested this month.  Then if a user has 1
    suggestion remaining they can either suggest a snack from the list or 
    input a name and location of a snack of their own.  

    On submit this does to the suggest_snack() function.
    """
    snacks = get_snacks()
    error_code = 0
    out_of_suggestions = False

    if snacks == 'API Error':
        error_code = -4
        snack_options = []
        create_cookie = False
    else:
        if 'suggestions_remaining' in request.COOKIES:
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

    response = render(
        request,
        'suggestions.html', {
            'snack_options': snack_options,
            'error_code': error_code,
        }
    )

    if create_cookie:
        response.set_cookie('suggestions_remaining', 1)
    if out_of_suggestions:
        response.set_cookie('suggestions_remaining', 0)

    return response


def suggest_snack(request):
    """Add a suggested snack to the API.
    This is the endpoint when a user clicks to add a suggested snack.

    /suggestions/suggest_snack/.

    Once this function is called it checks to see what data has been submitted
    and if the data is good it will initiate a POST request to the API with
    the provided snack name and snack location.  It will the provide an error
    code which corresponds to a message that is shown on the suggestions page.

    error_code == 1:
      The user successfully inputs a new suggestion.
    error_code == -1:
      The user has no suggestions remaining.
    error_code == -2:
      The user attempted to input a duplicate suggestion.
    error_code == -3:
      The user has not entered enough information.
    error_code == -4:
      The API is down for maintenance.

    After the suggested snack has been examined it calls the suggestions()
    function.
    """
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

            if error_code == 1:
                output = post_snacks(suggestion_input, suggestion_location)

                if output == 'API Error':
                    error_code = -4
        elif ((snack_option is None and suggestion_input == '' and
                suggestion_location == '') or (suggestion_input == '' and not
              suggestion_location == '') or (not suggestion_input == '' and
              suggestion_location == '')):
            error_code = -3

    response = HttpResponseRedirect('/suggestions/')

    if error_code == 1:
        response.set_cookie('suggestions_remaining', 0)
    else:
        response.set_cookie('suggestions_remaining', error_code)

    return response
