from django.db import models


class Snack(models.Model):
    """The Snack class records total votes of suggested snack items"""
    name = models.CharField(max_length=200, unique=True)
    votes = models.IntegerField(default=0)
