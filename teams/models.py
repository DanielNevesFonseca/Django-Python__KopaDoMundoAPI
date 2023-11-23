from django.db import models


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=30, null=False)
    titles = models.IntegerField(default=0)
    top_scorer = models.CharField(max_length=50, null=False)
    fifa_code = models.CharField(max_length=3, unique=True, null=False)
    first_cup = models.DateField()
