from django.urls import path

from . import views

urlpatterns = [
    path('vote/', views.voting, name='voting'),
    path('suggest/', views.suggestions, name='suggestions'),
]
