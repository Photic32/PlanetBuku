from django.contrib import admin
from django.urls import path, include
from .views import show_page, get_all_user_json, get_user_json, show_peminjam_individu

app_name = "daftar_peminjam"

urlpatterns = [
    path("", show_page, name="show_page"),
    path('all_user_json/', get_all_user_json, name='get_all_user_json'),
    path('user_json/<int:id>', get_user_json, name='get_user_json'),
    path('peminjam/<int:id>', show_peminjam_individu, name='show_peminjam_individu')
]