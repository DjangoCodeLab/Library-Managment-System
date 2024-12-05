from random import choice
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User




# Create your models here.
user_choice = [
    ('Admin','Admin'),
    ('Librarian','Librarian'),
    ('Member','Member')
]

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures',null = True, blank = True)
    bio = models.TextField(null = True, blank = True)
    role = models.CharField(max_length = 50,choices= user_choice, default='Member')


    def __str__(self):
        return self.user.username


class Book(models.Model):

    book_id = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    average_rating = models.DecimalField(max_digits=3,decimal_places=2)
    language_code =models.CharField(max_length = 10)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=500)
    price = models.IntegerField(default=100)


    def __str__(self):
        return self.title