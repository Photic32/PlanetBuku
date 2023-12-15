import json
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from book.models import Book
from edit_info.forms import BookForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET, require_POST


def get_books_json(request):
    data = Book.objects.filter()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@staff_member_required
def show_editInfo(request):
    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(request, "button.html", context)

def delete_book(request, id):
    # Dapatkan data buku berdasarkan ID
    book = Book.objects.get(pk=id)
    
    if request.method == "POST":
        # Hapus data buku dari database
        book.delete()
        return HttpResponseRedirect(reverse('edit_info:show_editInfo'))
    
    return render(request, "confirmation_template.html", {'book': book})

@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        publication_year = request.POST.get("publication_year")
        publisher = request.POST.get("publisher")
        isbn = request.POST.get("isbn")
        image_s = request.POST.get("image_s")
        image_m = request.POST.get("image_m")
        image_l = request.POST.get("image_l")
        stock = request.POST.get("stock")
        new_book = Book(title=title, author=author, publisher=publisher, publication_year=publication_year, isbn=isbn, image_s=image_s,  image_m=image_m, image_l=image_l, stock=stock )
        new_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def edit_book_form(request, id):
    # Get data buku berdasarkan ID
    data = Book.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = BookForm(request.POST or None, instance=data)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('edit_info:show_editInfo'))

    context = {'form': form,
                'book' : data
               }
    return render(request, "edit_info.html" , context)

@csrf_exempt
def edit_book(request, id):
    # Get data buku berdasarkan ID
    try:
        data = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return HttpResponseNotFound("Buku tidak ditemukan")

    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")
        publication_year = request.POST.get("publication_year")
        publisher = request.POST.get("publisher")
        isbn = request.POST.get("isbn")
        image_s = request.POST.get("image_s")
        image_m = request.POST.get("image_m")
        image_l = request.POST.get("image_l")
        stock = request.POST.get("stock")
        data.title = title
        data.author = author
        data.publication_year=publication_year
        data.publisher=publisher
        data.isbn=isbn
        data.image_s=image_s
        data.image_m=image_m
        data.image_l=image_l
        data.stock=stock

        data.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def increment_stock(request, id):
    data = get_object_or_404(Book, pk=id)
    
    data.stock += 1
    data.save()
    
    return HttpResponseRedirect(reverse('edit_info:show_editInfo'))

def decrement_stock(request, id):
    data = get_object_or_404(Book, pk=id)
    
    if data.stock > 0:
        data.stock -= 1
        data.save()
    
    return HttpResponseRedirect(reverse('edit_info:show_editInfo'))

@csrf_exempt
def delete_book_ajax(request, id):
    if request.method == 'POST':
        try:
            data = Book.objects.get(id=id)
            data.delete()
            return HttpResponse("OK", status=200)
        except Book.DoesNotExist:
            return HttpResponse("Buku tidak ada", status=404)

    return HttpResponseNotFound()

@csrf_exempt
def create_book_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_book = Book.objects.create(
            # user = request.user,
            title = data["title"],
            stock = int(data["stock"]),
            author = data["author"],
            publication_year  = int(data["publication_year"]),
            publisher  = data["publisher"],
            isbn  = data["isbn"],
            image_s  = data["image_s"],
            image_m  = data["image_m"],
            image_l  = data["image_l"],
            )
               

        new_book.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    

@csrf_exempt
def edit_book_flutter(request, id):
    try:
        data = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Buku tidak ditemukan"}, status=404)

    if request.method == 'POST':
        try:
            updated_data = json.loads(request.body)
            title = updated_data["title"]
            author = updated_data["author"]
            publication_year = updated_data["publication_year"]
            publisher = updated_data["publisher"]
            isbn = updated_data["isbn"]
            image_s = updated_data["image_s"]
            image_m = updated_data["image_m"]
            image_l = updated_data["image_l"]
            stock = updated_data["stock"]

            if(title!=""):
                data.title = title
            if(author!=""):
                data.author = author
            if(publication_year!="" and publication_year!="0"):
                data.publication_year = int(publication_year)
            if(publisher!=""):
                data.publisher = publisher
            if(isbn!=""):
                data.isbn = isbn
            if(image_s!=""):
                data.image_s = image_s
            if(image_m!=""):
                data.image_m = image_m
            if(image_l!=""):
                data.image_l = image_l
            if(stock!="0" and stock !=""):
                data.stock = int(stock)

            data.save()

            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Format JSON tidak valid"}, status=400)
    else:
        return JsonResponse({"status": "error"}, status=401)
    