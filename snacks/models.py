from django.db import models


class Snack(models.Model):
    name = models.CharField(max_length=200, unique=True)
    votes = models.IntegerField(default=0)
