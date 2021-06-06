from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.lookups import Transform

# Create your models here.

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):

    class Status(models.TextChoices):
        'AVAILABLE'
        'BORROWED'
        'RESERVED'
        'UNAVAILABLE'

    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    page_count = models.IntegerField()
    published_date = models.DateTimeField()
    image = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    authors = models.CharField(max_length=500)
    status = models.CharField(max_length=12, choices=Status, default='AVAILABLE')

    def __str__(self):
        return f"{self.title} by {self.authors} is {self.status}"


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duedate = models.DateTimeField()

    def __str__(self):
        return f"{self.user} borrows book {self.book} at {self.timestamp}"


class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duedate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} reserves book {self.book} at {self.timestamp}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=16)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} made a ${self.amount} payment at {self.timestamp}"


class Review(models.Model):

    class Rate(models.IntegerChoices):
        BAD = 1
        POOR = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=Rate.choices, blank=True, null=True)
    details = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} give a {self.rate} rating for book {self.book} at {self.timestamp}"