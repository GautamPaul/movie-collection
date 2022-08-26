from operator import mod
import uuid
from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key = True, editable = False)

    def __str__ (self):
        return self.title

class Collection(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key = True, default=uuid.uuid4, editable = False)
    description = models.CharField(max_length=1000)
    movies = models.ManyToManyField(Movie)
    
    def __str__ (self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    collection = models.ManyToManyField(Collection)

    def __str__ (self):
        return self.username