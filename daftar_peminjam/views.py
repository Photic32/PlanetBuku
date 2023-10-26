from django.shortcuts import render
from .models import Peminjam, Peminjaman
from book.models import Book
#import serialize
from django.core import serializers
from django.http import HttpResponse
import json
# Create your views here.
 

def serialize_semua_peminjam(semua_user):
    res = []
    for peminjam in semua_user:
        temp = {
            'username' : peminjam.user.username,
            'jumlah_buku_dipinjam' : peminjam.jumlah_buku_dipinjam,
            'pengembalian_paling_awal' : str(peminjam.pengembalian_paling_awal),
            'denda' : 69
        }
        res.append(temp)
    return json.dumps(res)

def get_all_user_json(request):
    semua_user = Peminjam.objects.all()
    return HttpResponse(serialize_semua_peminjam(semua_user))

def serialize_peminjam_individu(peminjam):
    buku_pinjam = []
    for peminjaman in peminjam.book_list.all():
        book = peminjaman.buku
        temp2 = {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "publication_year": book.publication_year,
            "publisher": book.publisher,
            "image_s": book.image_s,
            "image_m": book.image_m,
            "image_l": book.image_l,
            "stock": book.stock
        }
        buku_pinjam.append(temp2)
        
    temp = {
        'username' : peminjam.user.username,
        'jumlah_buku_dipinjam' : peminjam.jumlah_buku_dipinjam,
        'pengembalian_paling_awal' : str(peminjam.pengembalian_paling_awal),
        'denda' : 69,
        'buku_dipinjam' : buku_pinjam
    }
    return json.dumps(temp)

#tes git merge
def get_user_json(request, id):
    user = Peminjam.objects.get(pk=id)
    return HttpResponse(serialize_peminjam_individu(user))

def show_peminjam_individu(request, id):    
    return render(request, "peminjam.html", {"id": id})

def show_page(request):
    return render(request, "main.html")


