from django.shortcuts import render
from .models import Peminjam, Peminjaman
from book.models import Book
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .forms import PeminjamanForm
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST



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
@staff_member_required
def get_all_user_json(request):
    semua_user = Peminjam.objects.all()
    return HttpResponse(serialize_semua_peminjam(semua_user))

#peminjam.html
@staff_member_required
def get_pinjaman_json(request, id):
    pinjaman = Peminjaman.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", pinjaman))

@staff_member_required
def show_peminjam_individu(request, id):    
    context = {
        "peminjam": Peminjam.objects.get(pk=id),
        "username": Peminjam.objects.get(pk=id).user.username,
        "id": id
    }
    return render(request, "peminjam.html", context=context)

@staff_member_required
def show_page(request):
    semua_user = Peminjam.objects.all()
    context = {
        "jumlah_peminjam": len(semua_user)
    }
    return render(request, "main.html", context=context)

@staff_member_required
@require_POST
def edit_peminjaman(request, id):
    # Get berdasarkan ID
    peminjaman = Peminjaman.objects.get(pk = id)
    new_tanggal_pengembalian = None
    try:
        new_tanggal_pengembalian = datetime.strptime(request.POST['tanggal_pengembalian'], "%Y-%m-%d")
    except:
        return HttpResponseBadRequest("Invalid Input")
    if new_tanggal_pengembalian.date() < peminjaman.tanggal_pengembalian:
        return HttpResponseBadRequest("Tidak boleh memperpendek deadline")
    
    form = PeminjamanForm(request.POST or None, instance=peminjaman)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponse("Peminjam Edited Successfully")
    else:
        return HttpResponseBadRequest("Invalid Input")
    
@staff_member_required
def kembali_buku(request, id):
    # Get berdasarkan ID
    peminjaman = Peminjaman.objects.get(pk = id)
    peminjaman.status = "dikembalikan"
    peminjaman.save()
    return HttpResponse("Buku berhasil dikembalikan")  

@staff_member_required
@require_GET
def search_buku(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        title = request.GET.get("title")
        author = request.GET.get("author")
        isbn = request.GET.get("isbn")
        year = request.GET.get("year")
        publisher = request.GET.get("publisher")
        

        request.session['last_search'] = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'year': year,
            'publisher': publisher
        }
        
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
