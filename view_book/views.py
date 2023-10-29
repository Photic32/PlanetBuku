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
    queryset = Book.objects.all()

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
        return Book.objects.filter(title__icontains=query)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

def add_to_cart_ajax(request, book_pk):
    if request.method == 'POST':
        user = request.user
        keranjang = get_object_or_404(Keranjang, user=user)
        book = Book.objects.filter(pk=book_pk).first()
        if book in keranjang.book_list.all():
            return HttpResponseBadRequest("You have added book this to your cart")
        else:
            keranjang.book_list.add(book)
            keranjang.jumlah_buku = keranjang.book_list.count()
            keranjang.save()
            return HttpResponse(status=201)

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
        book = Book.objects.get(pk=book_pk)
        review = request.POST.get("review")
        rate = request.POST.get("rate")
        user = request.user
        try:
            if int(rate) < 0 or int(rate) > 5:
                return HttpResponseBadRequest("Invalid 'rate' value. Rate must be between 0 and 5.")
        except:
            return HttpResponseBadRequest("Invalid 'rate' value. Rate must be between 0 and 5.")
        

        new_review = Review(book=book, user=user, review=review, rate=rate)
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