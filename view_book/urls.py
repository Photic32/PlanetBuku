from django.urls import path
from view_book import views
from view_book.views import search_results, get_review_json, add_review_ajax

app_name = 'view_book'

urlpatterns = [
    path('', views.ViewBooks.as_view(), name='view_books'),
    path('search-books/', views.BookSearchView.as_view(), name='search_books'),
    path('search/', search_results, name="search"),
    path('<pk>/', views.ViewBook.as_view(), name="single_book_view"),
    path('get-review/', get_review_json, name='get_review_json'),
    path('create-review-ajax/', add_review_ajax, name='add_review_ajax')
]