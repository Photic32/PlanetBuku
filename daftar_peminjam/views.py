from django.shortcuts import render
from .models import Peminjam, Peminjaman
from book.models import Book
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from .forms import PeminjamanForm
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST


#
def serialize_semua_peminjam(semua_user):
  res = []
  for peminjam in semua_user:
    temp = {
        'username': peminjam.user.username,
        'user_id': peminjam.pk,
        'jumlah_buku_dipinjam': peminjam.jumlah_buku_dipinjam,
        'denda': 69
    }
    res.append(temp)
  return json.dumps(res)


#main.html
@staff_member_required
@csrf_exempt
def get_all_user_json(request):
  semua_user = Peminjam.objects.all()
  print(request.COOKIES)
  return HttpResponse(serialize_semua_peminjam(semua_user))


#peminjam.html
@staff_member_required
@csrf_exempt
def get_pinjaman_json(request, id):
  pinjaman = Peminjaman.objects.filter(pk=id)
  return HttpResponse(serializers.serialize("json", pinjaman))


@csrf_exempt
@staff_member_required
def show_peminjam_individu(request, id):
  context = {
      "peminjam": Peminjam.objects.get(pk=id),
      "username": Peminjam.objects.get(pk=id).user.username,
      "id": id
  }
  return render(request, "peminjam.html", context=context)


@csrf_exempt
@staff_member_required
def show_page(request):
  semua_user = Peminjam.objects.all()
  context = {"jumlah_peminjam": len(semua_user)}
  return render(request, "main.html", context=context)


@staff_member_required
@require_POST
@csrf_exempt
def edit_peminjaman(request, id):
  # Get berdasarkan ID
  data = json.loads(request.body)
  peminjaman = Peminjaman.objects.get(pk=id)
  new_tanggal_pengembalian = None
  try:
    new_tanggal_pengembalian = datetime.strptime(
        data['tanggal_pengembalian'], "%Y-%m-%d")
  except:
    return HttpResponseBadRequest("Invalid Input")
  if new_tanggal_pengembalian.date() < peminjaman.tanggal_pengembalian:
    return HttpResponseBadRequest("Tidak boleh memperpendek deadline")

  #get object by id
  peminjaman.tanggal_pengembalian = new_tanggal_pengembalian
  #save
  peminjaman.save()
  return JsonResponse({"res": "Buku berhasil diperpanjang"})



@csrf_exempt
@staff_member_required
def kembali_buku(request, id):
  # Get berdasarkan ID
  peminjaman = Peminjaman.objects.get(pk=id)
  peminjaman.status = "dikembalikan"
  peminjaman.save()
  return JsonResponse({"res": "Buku berhasil dikembalikan"})


@staff_member_required
@csrf_exempt
@require_GET
def search_buku(request):
  if request.method == "GET":
    user_id = request.GET.get("user_id")
    query = request.GET.get("query")

    hasil = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
        | Q(isbn__icontains=query) | Q(publication_year__icontains=query)
        | Q(publisher__icontains=query))
    pinjaman_List = []
    list_pinjaman = Peminjam.objects.get(pk=user_id).book_list.all()
    for pinjaman in list_pinjaman:
      if (pinjaman.buku in hasil):
        pinjaman_List.append(pinjaman)

    buku_pinjam = []
    for peminjaman in pinjaman_List:
      tempBuku = peminjaman.buku
      temp2 = {
          "deadline": str(peminjaman.tanggal_pengembalian),
          "status": peminjaman.status,
          "isbn": tempBuku.isbn,
          "title": tempBuku.title,
          "author": tempBuku.author,
          "image": tempBuku.image_s,
          "peminjaman_id": peminjaman.pk
      }
      buku_pinjam.append(temp2)
    peminjam = Peminjam.objects.get(pk=user_id)
    temp = {
        'username': peminjam.user.username,
        'jumlah_buku_dipinjam': peminjam.jumlah_buku_dipinjam,
        'buku_dipinjam': buku_pinjam
    }
    return HttpResponse(json.dumps(temp))
