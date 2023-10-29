from django.urls import path
from borrowed_book_list.views import borrowed_book_list, add_kesan_ajax, get_kesan_json, return_book, borrowed_book_json
app_name = 'borrowed_book_list'

urlpatterns = [
    path('', borrowed_book_list, name='borrowed_book_list'),
    path('return-book/<int:book_id>', return_book, name='return_book'),
    path('get-kesan/<int:id>', get_kesan_json, name='get_kesan_json'),
    path('create-kesan-ajax/', add_kesan_ajax, name='add_kesan_ajax'),
    path('borrowed-book-json/', borrowed_book_json, name='borrowed_book_json')
]