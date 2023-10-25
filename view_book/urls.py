from django.urls import path
from view_book.views import view_books

app_name = 'main'

urlpatterns = [
    path('', view_books, name='view_books'),
]