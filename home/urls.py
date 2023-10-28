from django.urls import path
from home.views import register, logout_user, show_home, get_book_json, get_peminjaman_json, get_keranjang_json
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

app_name='home'

urlpatterns = [
    path('', show_home, name='show_home'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('get-product/', get_book_json, name='get_book_json'),
    path('get-peminjaman/', get_peminjaman_json, name='get_peminjaman_json'),
    path('get-keranjang/', get_keranjang_json, name='get_keranjang_json'),
]