from django.urls import path

from . import views

urlpatterns = [
    path('voting/', views.voting, name='voting'),
    path('suggestions/', views.suggestions, name='suggestions'),
]
