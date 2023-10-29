from django.db import models
from django.contrib.auth.models import User
from book.models import Book
from datetime import timedelta
from django.utils import timezone

from borrowed_book_list.models import Peminjaman
# Create your models here.

def in_seven_days():
    return timezone.now() + timedelta(days=7)

#dummy

class Peminjam(models.Model): # App 1
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_list = models.ManyToManyField(Peminjaman,  blank=True)
    jumlah_buku_dipinjam = models.IntegerField(default=0)
    