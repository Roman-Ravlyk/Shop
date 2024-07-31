from django.db import models
from django.contrib.auth.models import User
from Sneakers.models import Sneakers

class UserBuyHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sneakers = models.ForeignKey(Sneakers, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, sneakers: {self.sneakers.name}"