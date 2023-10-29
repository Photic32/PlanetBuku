from django.db import models
from book.models import Book
from django.utils.timezone import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

def in_seven_days():
    return timezone.now() + timedelta(days=7)

class Peminjaman(models.Model): # App 5
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_peminjaman = models.DateField(auto_now_add=True)
    tanggal_pengembalian = models.DateField(null=True, blank=True)
    buku = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')])

class KesanPeminjam(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    kesan = models.TextField()
# Create your models here.
