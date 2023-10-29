from django.contrib import admin
from .models import Peminjaman, Peminjam

@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ['pengguna', 'tanggal_peminjaman', 'tanggal_pengembalian', 'buku', 'status']

@admin.register(Peminjam)
class PeminjamAdmin(admin.ModelAdmin):
    list_display = ['user', 'jumlah_buku_dipinjam']

