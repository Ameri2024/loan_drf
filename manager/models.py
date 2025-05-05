from django.db import models
from accounts.models import MyUser
from django_jalali.db import models as jalali_models

class SaveBalance(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='save_balance')
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} {self.balance}'


class AdminPosts(models.Model):
    auther = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='admin_posts')
    subject = models.CharField(max_length=200)
    post = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.subject} - {self.created}'

