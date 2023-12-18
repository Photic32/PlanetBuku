from django.contrib import admin
from django.urls import path, include
from edit_info.views import get_books_json, show_editInfo, edit_book, delete_book, delete_book_ajax
from edit_info.views import increment_stock, decrement_stock, add_book_ajax, edit_book_form, create_book_flutter, edit_book_flutter
from django.conf import settings
from django.conf.urls.static import static

app_name = "edit_info"

urlpatterns = [
    path("", show_editInfo, name="show_editInfo"),
    path('get_books_json/', get_books_json, name='get_books_json'),
    path('edit_book/<int:id>', edit_book, name='edit_book'),
    path('delete_book/<int:id>', delete_book, name='delete_book'),
    path('add_book_ajax/', add_book_ajax, name='add_book_ajax'),
    path('delete_book_ajax/<int:id>/', delete_book_ajax, name='delete_book_ajax'),
    path('increment_stock/<int:id>/', increment_stock, name='increment_stock'),
    path('decrement_stock/<int:id>/', decrement_stock, name='decrement_stock'),
    path('edit_book_form/<int:id>', edit_book_form, name='edit_book_form'),
    path('create-flutter/', create_book_flutter, name='create_book_flutter'),
    path('edit-flutter/<int:id>/', edit_book_flutter, name='edit_book_flutter'),
]
