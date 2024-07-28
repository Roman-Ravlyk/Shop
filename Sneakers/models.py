from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sneakers(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    appointment = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name

