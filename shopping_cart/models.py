from django.db import models
from django.contrib.auth.models import User
from Sneakers.models import Sneakers, Brand

class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sneakers = models.ForeignKey(Sneakers, on_delete=models.CASCADE)

    def __str__(self):
        return f"user_id: {self.user.username}, sneakers_id: {self.sneakers.name}"