from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrowed_book_list.models import Peminjaman, KesanPeminjam
from book.models import Book
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@login_required
def borrowed_book_list(request):
    peminjaman_dipinjam = Peminjaman.objects.filter(pengguna=request.user, status =('dipinjam'))
    peminjaman_dikembalikan = Peminjaman.objects.filter(pengguna=request.user, status =('dikembalikan'))
    context = {
        'peminjaman_dipinjam' : peminjaman_dipinjam,
        'peminjaman_dikembalikan' : peminjaman_dikembalikan,
    }

    return render(request, "borrowed_book_list.html", context)

@login_required
def return_book(request, book_id):
    # Retrieve the book object by its ID.
    peminjaman = get_object_or_404(Peminjaman, pk=book_id)

    # Check if the book is currently marked as "dipinjam."
    if peminjaman.status == 'dipinjam':
        # Update the status to "dikembalikan."
        peminjaman.status = 'dikembalikan'
        peminjaman.save()
        # return HttpResponse("Book marked as returned successfully.")
        # return HttpResponseNotFound()
    return HttpResponseRedirect(reverse('borrowed_book_list:borrowed_book_list'))


@csrf_exempt
# def add_kesan_ajax(request,id):
#     if request.method == 'POST':
#         # book = request.book
#         peminjaman = get_object_or_404(Peminjaman, pk=id)
#         book_id = request.POST.get("book_id")
#         kesan = request.POST.get("kesan")
#         # book = get_object_or_404(Book, pk=book_id)
#         new_kesan = KesanPeminjam(peminjaman=peminjaman, kesan=kesan)
#         new_kesan.save()

#         return HttpResponse(b"CREATED", status=201)

#     return HttpResponseNotFound()
def add_kesan_ajax(request):
    if request.method == 'POST':
        # book = request.book
        book_id = request.POST.get("book_id")
        kesan = request.POST.get("kesan")
        book = get_object_or_404(Book, pk=book_id)
        new_kesan = KesanPeminjam(book=book, kesan=kesan)
        new_kesan.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_kesan_json(request):
    book = get_object_or_404(Book, pk=id)
    kesan_peminjam = KesanPeminjam.objects.filter(book=book)
    return HttpResponse(serializers.serialize('json', kesan_peminjam))
    
# Create your views here.