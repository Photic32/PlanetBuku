from django.contrib import admin
from django.urls import path, include
from .views import show_page, get_all_user_json, show_peminjam_individu,\
      edit_peminjaman, search_buku, kembali_buku, get_pinjaman_json

app_name = "daftar_peminjam"

urlpatterns = [
    path("", show_page, name="show_page"),
    path('all_user_json/', get_all_user_json, name='get_all_user_json'),
    path('pinjaman_json/<int:id>', get_pinjaman_json, name='get_pinjaman_json'),
    path('peminjam/<int:id>', show_peminjam_individu, name='show_peminjam_individu'),
    path('edit_peminjaman/<int:id>', edit_peminjaman, name='edit_peminjaman'),
    path('search_book/', search_buku, name='search_buku'),
    path('kembali_buku/<int:id>', kembali_buku, name='kembali_buku'),
]