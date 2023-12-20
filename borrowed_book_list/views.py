from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrowed_book_list.models import Peminjaman, KesanPeminjam
from book.models import Book
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib.auth.models import User

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

def borrowed_book_byid(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    peminjaman_dipinjam = Peminjaman.objects.filter(pengguna=user, status=('dipinjam'))
    peminjaman_dikembalikan = Peminjaman.objects.filter(pengguna=user, status =('dikembalikan'))
    serialized_books = serialize_peminjam_individu(peminjaman_dipinjam, peminjaman_dikembalikan)
    # return HttpResponse(serializers.serialize('json', peminjaman_dipinjam))

    return HttpResponse(serialized_books, content_type='application/json')


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
        print(kesantext)
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
    # return HttpResponseRedirect(reverse('borrowed_book_list:borrowed_book_list'))
    return JsonResponse({"success" : "True"})

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


@csrf_exempt
def add_kesan_flutter(request, id):
    try:
        data = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Buku tidak ditemukan"}, status=404)

    if request.method == 'POST':
        try:
            updated_data = json.loads(request.body)

            data.kesan = updated_data["kesan"]
            book = get_object_or_404(Book, pk=id)

            new_kesan = KesanPeminjam(book=book, kesan=updated_data['kesan'])
            new_kesan.save()
            

            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Format JSON tidak valid"}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=401)
# Create your views here.