from django.db import models
from book.models import Book
from django.contrib.auth.models import User

class Peminjaman(models.Model): # App 5
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal_peminjaman = models.DateField(auto_now_add=True)
    tanggal_pengembalian = models.DateField(null=True, blank=True)
    buku = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')])

    def save(self, *args, **kwargs):
        if self.tanggal_pengembalian is None:
            self.tanggal_pengembalian = self.tanggal_peminjaman.date() + datetime.timedelta(days=7)
        super(Peminjaman, self).save(*args, **kwargs)
# Create your models here.
