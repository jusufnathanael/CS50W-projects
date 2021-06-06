from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    closed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, price: ${self.price} (active: {self.active})"


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bids the item {self.item} with price ${self.price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    details = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented for item {self.item} at {self.date}: {self.details}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user} watches the item {self.item}"

