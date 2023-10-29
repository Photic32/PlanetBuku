from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrowed_book_list.models import Peminjaman, KesanPeminjam
from book.models import Book
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

def borrowed_book_list(request):
    peminjaman_dipinjam = Peminjaman.objects.filter(pengguna=request.user, status =('dipinjam'))
    peminjaman_dikembalikan = Peminjaman.objects.filter(pengguna=request.user, status =('dikembalikan'))
    context = {
        'peminjaman_dipinjam' : peminjaman_dipinjam,
        'peminjaman_dikembalikan' : peminjaman_dikembalikan,
    }

    return render(request, "borrowed_book_list.html", context)



def borrowed_book_json(request):
    peminjaman_dipinjam = Peminjaman.objects.filter(pengguna=request.user, status =('dipinjam'))
    peminjaman_dikembalikan = Peminjaman.objects.filter(pengguna=request.user, status =('dikembalikan'))
    return HttpResponse(serialize_peminjam_individu(peminjaman_dipinjam, peminjaman_dikembalikan))

#peminjam.html
def serialize_peminjam_individu(peminjaman_dipinjam, peminjaman_dikembalikan):
    dipinjam = []
    dikembalikan = []
    for peminjaman in peminjaman_dipinjam:
        book = peminjaman.buku
        kesan = KesanPeminjam.objects.filter(book=book)
        kesantext = "Tidak Ada kesan ^_^"
        for k in kesan:
            kesantext = k.kesan 
        temp2 = {
            "deadline" : str(peminjaman.tanggal_pengembalian),
            "status" : peminjaman.status,
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "image": book.image_s,
            "peminjaman_id" : peminjaman.pk,
            "book_id" : book.pk,
            "kesan" : kesantext
        }
        dipinjam.append(temp2)
    for peminjaman in peminjaman_dikembalikan:
        book = peminjaman.buku
        kesan = KesanPeminjam.objects.filter(book=book)
        kesantext = "Tidak Ada kesan ^_^"
        for k in kesan:
            kesantext = k.kesan 
        # kesan = KesanPeminjam.objects.filter(book=book).last()
        # if(kesan is None):
        #     kesan = "kesan kosong"
        # else:
        #     kesan = kesan.kesan    
        temp2 = {
            "deadline" : str(peminjaman.tanggal_pengembalian),
            "status" : peminjaman.status,
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "image": book.image_s,
            "peminjaman_id" : peminjaman.pk,
            "book_id" : book.pk, 
            "kesan" : kesantext
        }
        dikembalikan.append(temp2)

    return json.dumps({'dipinjam': dipinjam, 'dikembalikan': dikembalikan})

def return_book(request, book_id):
    # Retrieve the book object by its ID.
    peminjaman = get_object_or_404(Peminjaman, pk=book_id)

    # Check if the book is currently marked as "dipinjam."
    if peminjaman.status == 'dipinjam':
        # Update the status to "dikembalikan."
        peminjaman.status = 'dikembalikan'
        peminjaman.save()
        # return HttpResponse("Book marked as returned successfully.")
    return HttpResponseRedirect(reverse('borrowed_book_list:borrowed_book_list'))

@csrf_exempt
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

def get_kesan_json(request, id):
    book = get_object_or_404(Book, pk=id)
    kesan_peminjam = KesanPeminjam.objects.filter(book=book)
    if(kesan_peminjam.count() == 0):
        return HttpResponseNotFound('No feedback found.')
    # else:
    #     kesan_peminjam = kesan_peminjam[0]
    return HttpResponse(serializers.serialize('json', kesan_peminjam))
    
# Create your views here.