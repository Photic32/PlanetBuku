from django.urls import path
from borrowed_book_list.views import borrowed_book_list, add_kesan_ajax, get_kesan_json, return_book
app_name = 'borrowed_book_list'

urlpatterns = [
    path('', borrowed_book_list, name='borrowed_book_list'),
    path('return-book/<int:book_id>', return_book, name='return_book'),
    path('get-kesan/', get_kesan_json, name='get_kesan_json'),
    path('create-kesan-ajax/', add_kesan_ajax, name='add_kesan_ajax')
]