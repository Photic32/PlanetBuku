from typing import Any
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import datetime
from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser, PermissionsMixin, AbstractUser, BaseUserManager

class Book(models.Model): # App 2
    isbn = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    publisher = models.TextField(null=True, blank=True)
    image_s = models.TextField(null=True, blank=True)
    image_m = models.TextField(null=True, blank=True)
    image_l = models.TextField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)

class Review(models.Model): # App 3
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rate = models.IntegerField()
    review_date = models.DateField(auto_now_add=True)

class Keranjang(models.Model): # App 4
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_list = models.ManyToManyField(Book)
    jumlah_buku = models.IntegerField(default=0)

class Peminjam(models.Model): # App 1
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_list = models.ManyToManyField(Book)
    jumlah_buku_dipinjam = models.IntegerField(default=0)