from django.shortcuts import render
from book.models import Book

def view_books(request):
    books = Book.objects.all()
    
    context = {
        'books': books,
    }

    return render(request, "view_books.html", context)
