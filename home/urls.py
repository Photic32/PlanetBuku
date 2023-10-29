from django.urls import path
from home.views import register, logout_user, show_home, get_book_json, get_peminjaman_json, get_keranjang_json, submit_cart, show_keranjang, getBukuKeranjang_json, get_bukuPeminjaman_json, get_reviews_json, get_bukuReviews_json, remove_cart, show_profile
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
    path('get-reviews', get_reviews_json, name='get_reviews_json'),
    path('submit-cart/', submit_cart, name='submit_cart'),
    path('remove-cart/', remove_cart, name='remove_cart'),
    path('cart/', show_keranjang, name='show_keranjang'),
    path('get-buku-keranjang', getBukuKeranjang_json, name='getBukuKeranjang_json'),
    path('get-buku-peminjaman', get_bukuPeminjaman_json, name='get_bukuPeminjaman_json'),
    path('get-reviews-peminjaman', get_bukuReviews_json, name='get_bukuReviews_json'),
    path('show-profile', show_profile, name='show_profile'),
]
