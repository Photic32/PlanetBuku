import json
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from book.models import Book
from view_book.forms import ReviewForm
from view_book.models import Review
from home.models import Keranjang
from django.views.decorators.csrf import csrf_exempt

class ViewBooks(ListView):
    paginate_by = 15
    model = Book
    template_name = 'view_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.order_by('id')

class ViewBook(DetailView):
    model = Book
    template_name = 'view_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            user = self.request.user
            book = context['book']
            has_reviewed = Review.objects.filter(book=book, user=user).exists()
            context['has_reviewed'] = has_reviewed
            context['review_form'] = ReviewForm()
        else:
            context['has_reviewed'] = False

        return context

class BookSearchView(ListView):
    paginate_by = 15
    model = Book
    template_name = 'view_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(title__icontains=query).order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

@csrf_exempt
def add_to_cart_ajax(request, book_pk):
    if request.method == 'POST' or request.method == 'GET':
        user = request.user
        keranjang = get_object_or_404(Keranjang, user=user)
        book = Book.objects.filter(pk=book_pk).first()
        if book in keranjang.book_list.all():
            return HttpResponse("Book is already in your cart", status=200)
        else:
            keranjang.book_list.add(book)
            keranjang.jumlah_buku = keranjang.book_list.count()
            keranjang.save()
            return HttpResponse(status=201)

    return HttpResponseNotFound()

@csrf_exempt
def add_to_cart_flutter(request, book_pk):
    if request.method == 'POST' or request.method == 'GET':
        user = request.user
        keranjang = get_object_or_404(Keranjang, user=user)
        book = Book.objects.filter(pk=book_pk).first()
        if book in keranjang.book_list.all():
            return JsonResponse({
                "status": False,
                "message": "You have added this book to your cart."
            }, status=200)
        else:
            keranjang.book_list.add(book)
            keranjang.jumlah_buku = keranjang.book_list.count()
            keranjang.save()
            return JsonResponse({
                "status": True,
                "message": "Added to cart!"
            }, status=200)

    return HttpResponseNotFound()

def get_review_json(request, book_pk):
    reviews_by_book = Review.objects.filter(book__pk=book_pk)
    data = [{
        'user': review.user.username,
        'review': review.review, 'rate': review.rate,
        'review_date': review.review_date} for review in reviews_by_book]
    return JsonResponse({'reviews': data})

@csrf_exempt
def give_review_ajax(request, book_pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_pk)
        review_text = request.POST.get("review")
        rate = request.POST.get("rate")
        user = request.user
        try:
            rate = int(rate)
            if rate < 0 or rate > 5:
                return HttpResponseBadRequest("Invalid 'rate' value. Rate must be between 0 and 5.")
        except ValueError:
            return HttpResponseBadRequest("Invalid 'rate' value. Rate must be an integer between 0 and 5.")

        existing_review = Review.objects.filter(book=book, user=user).first()

        if existing_review:
            existing_review.review = review_text
            existing_review.rate = rate
            existing_review.save()
            
            return HttpResponse("UPDATED", status=201)
        
        else:
            new_review = Review(book=book, user=user, review=review_text, rate=rate)
            new_review.save()

            return HttpResponse("CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def give_review_flutter(request, book_pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_pk)
        data = json.loads(request.body)

        review_text = data.get("review")
        rate = int(data.get("rate"))
        user = request.user
        existing_review = Review.objects.filter(book=book, user=user).first()

        if existing_review:
            existing_review.review = review_text
            existing_review.rate = rate
            existing_review.save()
            return JsonResponse({"status": "success", "existed": True}, status=200)
        
        else:
            new_review = Review(book=book, user=user, review=review_text, rate=rate)
            new_review.save()

            return JsonResponse({"status": "success", "existed": False}, status=200)
        
    else:
        return JsonResponse({"status": "error"}, status=401)

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