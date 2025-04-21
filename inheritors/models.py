from accounts.models import MyUser
from django.db import models


class Inheritors(models.Model):  # Persons who's heir from accounts
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    national_code = models.CharField(max_length=10)
    share_percent = models.SmallIntegerField(default=100)
    relation = models.CharField(max_length=200, blank=True)

    # relation to accounts

    def __str__(self):
        return f'{self.name}   {self.last_name} {self.user}'
