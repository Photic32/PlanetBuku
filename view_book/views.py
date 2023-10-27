from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from book.models import Book
from view_book.models import Review
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

class ViewBooks(ListView):
    paginate_by = 15
    model = Book
    template_name = 'view_books.html'
    context_object_name = 'books'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context data
        context['qo'] = None

        return context

class ViewBook(DetailView):
    model = Book
    template_name = 'view_detail.html'
    context_object_name = 'book'

class BookSearchView(ListView):
    paginate_by = 15
    model = Book
    template_name = 'view_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(title__icontains=query)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context data
        context['q'] = self.request.GET.get('q')
        return context

def get_review_json(request):
    reviews_by_book = Review.objects.filter(book=request.book)
    return HttpResponse(serializers.serialize('json', reviews_by_book))

@csrf_exempt
def add_review_ajax(request):
    if request.method == 'POST':
        book = request.book
        review = request.POST.get("review")
        rate = request.POST.get("rate")
        # user = request.user

        new_review = Review(book=book, review=review, rate=rate,)
        # new_review = Review(book=book, user = user, review=review, rate=rate,)
        new_review.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def search_results(request):
    if request.method == 'POST':
        book = request.POST.get('book')
        query = Book.objects.filter(title__icontains=book)
        if len(query) > 0 and len(book) > 0:
            data = []
            counter = 0
            for pos in query:
                item = {
                    'pk': pos.pk,
                    'title': pos.title,
                    'author': pos.author,
                }
                data.append(item)
                counter += 1
                if (counter == 5):
                    break
            res = data
        else:
            res = 'No books found'
        return JsonResponse({'data': res})
    return JsonResponse({})