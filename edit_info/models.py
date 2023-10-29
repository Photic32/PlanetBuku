from django.db import models
from django.contrib.auth.models import User

class Book(models.Model): # App 2
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    publisher = models.TextField(null=True, blank=True)
    isbn = models.TextField(null=True, blank=True)
    image_s = models.TextField(null=True, blank=True)
    image_m = models.TextField(null=True, blank=True)
    image_l = models.TextField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
