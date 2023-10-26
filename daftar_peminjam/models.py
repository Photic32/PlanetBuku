from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.

#dummy
class Peminjaman(models.Model): # App 5
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_peminjaman = models.DateField(auto_now_add=True)
    tanggal_pengembalian = models.DateField(null=True, blank=True)
    buku = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')])

class Peminjam(models.Model): # App 1
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_list = models.ManyToManyField(Peminjaman)
    pengembalian_paling_awal = models.DateField(null=True, blank=True)
    jumlah_buku_dipinjam = models.IntegerField(default=0)
    