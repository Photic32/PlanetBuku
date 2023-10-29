from django.contrib import admin
from .models import Peminjaman, Peminjam

@admin.register(Peminjam)
class PeminjamAdmin(admin.ModelAdmin):
    list_display = ['user', 'jumlah_buku_dipinjam']

