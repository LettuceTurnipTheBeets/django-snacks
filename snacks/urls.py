from django.urls import path

from . import views

urlpatterns = [
    path('voting/', views.voting, name='voting'),
    path('voting/vote/<name>/', views.vote, name='vote'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('suggestions/suggest_snack/', views.suggest_snack, name='suggest_snack'),
]
