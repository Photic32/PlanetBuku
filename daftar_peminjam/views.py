from django.shortcuts import render
from .models import Peminjam, Peminjaman
from book.models import Book
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .forms import PeminjamanForm
import json
from django.views.decorators.csrf import csrf_exempt
 
#main.html
def serialize_semua_peminjam(semua_user):
    res = []
    for peminjam in semua_user:
        temp = {
            'username' : peminjam.user.username,
            'user_id' : peminjam.pk,
            'jumlah_buku_dipinjam' : peminjam.jumlah_buku_dipinjam,
            'denda' : 69
        }
        res.append(temp)
    return json.dumps(res)

#main.html
def get_all_user_json(request):
    semua_user = Peminjam.objects.all()
    return HttpResponse(serialize_semua_peminjam(semua_user))

#peminjam.html
def get_pinjaman_json(request, id):
    pinjaman = Peminjaman.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", pinjaman))

def show_peminjam_individu(request, id):    
    context = {
        "peminjam": Peminjam.objects.get(pk=id),
        "username": Peminjam.objects.get(pk=id).user.username,
        "id": id
    }
    return render(request, "peminjam.html", context=context)

def show_page(request):
    semua_user = Peminjam.objects.all()
    context = {
        "jumlah_peminjam": len(semua_user)
    }
    return render(request, "main.html", context=context)

@csrf_exempt
def edit_peminjaman(request, id):
    # Get berdasarkan ID
    peminjaman = Peminjaman.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = PeminjamanForm(request.POST or None, instance=peminjaman)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponse("Peminjam Edited Successfully")
    else:
        return HttpResponseBadRequest("Error")
    
def kembali_buku(request, id):
    # Get berdasarkan ID
    peminjaman = Peminjaman.objects.get(pk = id)
    peminjaman.status = "dikembalikan"
    peminjaman.save()
    return HttpResponse("SIUUU")  

def search_buku(request):
    if request.method == "GET":
        title = request.GET.get("title")
        author = request.GET.get("author")
        isbn = request.GET.get("isbn")
        year = request.GET.get("year")
        publisher = request.GET.get("publisher")
        user_id = request.GET.get("user_id")
        hasil = Book.objects.filter(
            Q(title__icontains=title) & 
            Q(author__icontains=author) & 
            Q(isbn__icontains=isbn) & 
            Q(publication_year__icontains=year) & 
            Q(publisher__icontains=publisher)
        )
        pinjaman_List = []
        list_pinjaman = Peminjam.objects.get(pk=user_id).book_list.all()
        for pinjaman in list_pinjaman:
            if(pinjaman.buku in hasil):
                pinjaman_List.append(pinjaman)

        buku_pinjam = []
        for peminjaman in pinjaman_List:
            tempBuku = peminjaman.buku
            temp2 = {
                "deadline" : str(peminjaman.tanggal_pengembalian),
                "status" : peminjaman.status,
                "isbn": tempBuku.isbn,
                "title": tempBuku.title,
                "author": tempBuku.author,
                "image": tempBuku.image_s,
                "peminjaman_id" : peminjaman.pk
            }
            buku_pinjam.append(temp2)
        peminjam = Peminjam.objects.get(pk=user_id)
        temp = {
            'username' : peminjam.user.username,
            'jumlah_buku_dipinjam' : peminjam.jumlah_buku_dipinjam,
            'buku_dipinjam' : buku_pinjam
        }        
        return HttpResponse(json.dumps(temp))
