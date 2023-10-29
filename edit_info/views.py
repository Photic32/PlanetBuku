from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from book.models import Book
from edit_info.forms import BookForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required


def get_books_json(request):
    data = Book.objects.filter()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# @staff_member_required
def show_editInfo(request):
    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(request, "main.html", context)

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
