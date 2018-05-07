from django.db import models


class Snack(models.Model):
    """The Snack class records total votes of suggested snack items
    and the month it was most recently suggested.
    """
    name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    month_last_suggested = models.IntegerField(default=1)
