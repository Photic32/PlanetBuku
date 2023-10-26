from django.urls import path
from borrowed_book_list.views import borrowed_book_list
app_name = 'borrowed_book_list'

urlpatterns = [
    path('', borrowed_book_list, name='borrowed_book_list'),
]