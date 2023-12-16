import json
from django.shortcuts import render
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from book.models import Book
from home.models import Keranjang
from borrowed_book_list.models import Peminjaman
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.urls import reverse
from django.http import JsonResponse
from django.urls import reverse
from book.models import Book
from view_book.models import Review
from home.models import Keranjang
from daftar_peminjam.models import Peminjam
from borrowed_book_list.models import Peminjaman
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_book_json(request):
    books = Book.objects.filter(stock__gt=0)
    return HttpResponse(serializers.serialize('json', books))

def get_peminjaman_json(request):
    peminjamans = Peminjaman.objects.filter(pengguna=request.user)
    return HttpResponse(serializers.serialize('json', peminjamans))

def get_keranjang_json(request):
    keranjangs = Keranjang.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', keranjangs))

# @login_required(login_url='/register')
# def show_home(request):
#     user = request.user
#     if user.is_staff == True:
#         context = {
#             'last_login': request.COOKIES['last_login'],
#             'username' : user.username,
#         }


#         return render(request, "homeAdmin.html", context)
#     else:
#         context = {
#             'last_login': request.COOKIES['last_login'],
#             'username' : user.username,
#         }

#         return render(request, "homeUser.html", context)


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        if request.POST.get("submitButton") =="Register":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('home:register')
            else:
                messages.info(request, 'Sorry, incorrect username or password. Please try again.')
        elif request.POST.get("submitButton") =="Login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("home:show_home")) 
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {'form':form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('home:register'))
    response.delete_cookie('last_login')
    return response
# Create your views here.


def show_profile(request):
    if request.user.is_authenticated:
        user = request.user
        borrowedCount = Peminjaman.objects.filter(pengguna=request.user).count()
        reviewsCount = Review.objects.filter(user=request.user).count()
        cartCount = Keranjang.objects.filter(user=request.user)[0].jumlah_buku
            #kalo staff
        context = {
            'last_login': request.COOKIES['last_login'], 
            'username' : user.username,
            'borrowedCount' : borrowedCount,
            'reviewsCount' : reviewsCount,
            'cartCount' : cartCount,
        }

        return render(request, "profile.html", context)
 
    else:                                       #kalo guest
        return render(request,"homeGuest.html")

def get_bukuReviews_json(request):
    review = Review.objects.filter(user=request.user)
    bukuReview=[]
    for review1 in review:
        bukuReview.append(review1.book)
    
    return HttpResponse(serializers.serialize('json', bukuReview))

def get_reviews_json(request):
    reviews = Review.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', reviews))

def get_bukuPeminjaman_json(request):
    peminjaman = Peminjaman.objects.filter(pengguna=request.user)
    bukuKeranjang =[]
    for peminjaman1 in peminjaman:
        bukuKeranjang.append(peminjaman1.buku)
    
    return HttpResponse(serializers.serialize('json', bukuKeranjang))

def getBukuKeranjang_json(request):
    keranjang = Keranjang.objects.filter(user=request.user)[0]
    bukuKeranjang = keranjang.book_list.all()
    return HttpResponse(serializers.serialize('json', bukuKeranjang))

def getBukuKeranjangFlutter_json(request, id):
    keranjang = Keranjang.objects.filter(user=id)[0]
    bukuKeranjang = keranjang.book_list.all()
    return HttpResponse(serializers.serialize('json', bukuKeranjang))

def get_book_json(request):
    books = Book.objects.filter(stock__gt=0)
    return HttpResponse(serializers.serialize('json', books))

def get_peminjaman_json(request):
    peminjamans = Peminjaman.objects.filter(pengguna=request.user)
    return HttpResponse(serializers.serialize('json', peminjamans))

@login_required       #decorator login, gabisa diakses kalo ga login
def get_keranjang_json(request):
    keranjangs = Keranjang.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', keranjangs))

def show_keranjang(request):
    if request.user.is_authenticated:
        context = {
            'last_login': request.COOKIES['last_login'],
            'username' : request.user.username,
        }

        return render(request, "cart.html", context)
    else:                                     
        return render(request,"homeGuest.html")

@login_required(login_url='/register')
def show_home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_staff == True:               #kalo staff
            context = {
                'last_login': request.COOKIES['last_login'], 
                'username' : user.username,
            }

            return render(request, "homeAdmin.html", context)
        else:                                   #kalo user
            context = {
                'last_login': request.COOKIES['last_login'],
                'username' : user.username,
            }
            return render(request, "homeUser.html", context)
    else:                                       #kalo guest
        return render(request,"homeGuest.html")


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        if request.POST.get("submitButton") =="Register":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                newKeranjang = Keranjang(user=user)
                newKeranjang.save()
                newPeminjam = Peminjam(user=user)
                newPeminjam.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('home:register')
            else:
                messages.info(request, 'Sorry, incorrect username or password. Please try again.')
        elif request.POST.get("submitButton") =="Login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("home:show_home")) 
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {'form':form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('home:register'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def submit_cart(request):
    #handle keranjang
    if request.method =='POST':
        if request.POST.get('action') == 'cart_button':
            token = request.POST.get('csrfmiddlewaretoken')
            id=request.POST.get('id')
            keranjang = Keranjang.objects.filter(user=request.user)
            buku = Book.objects.filter(pk = id)
            newStockBuku = buku[0].stock - 1
            buku.update(stock=newStockBuku)
            keranjang[0].book_list.remove(buku[0])
            newJumlahKeranjang = keranjang[0].jumlah_buku - 1
            keranjang.update(jumlah_buku=newJumlahKeranjang)
            #handle peminjaman
            newPeminjaman=Peminjaman(pengguna=request.user, buku=buku[0], status='dipinjam')
            newPeminjaman.save()
            temp = Peminjaman.objects.filter(pengguna=request.user, buku=buku[0], status='dipinjam')
            #handle peminjam
            peminjam = Peminjam.objects.filter(user=request.user)
            peminjam[0].book_list.add(temp[0])
            newJumlahPeminjam = peminjam[0].jumlah_buku_dipinjam + 1
            peminjam.update(jumlah_buku_dipinjam=newJumlahPeminjam)
        
            return HttpResponse(b"ADDED", status=201)
        
@csrf_exempt
def remove_cart(request):
    #handle keranjang
    if request.method =='POST':
        if request.POST.get('action') == 'cart_del':
            token = request.POST.get('csrfmiddlewaretoken')
            id=request.POST.get('id')
            keranjang = Keranjang.objects.filter(user=request.user)
            buku = Book.objects.filter(pk = id)
            newStockBuku = buku[0].stock + 1
            buku.update(stock=newStockBuku)
            keranjang[0].book_list.remove(buku[0])
            newJumlahKeranjang = keranjang[0].jumlah_buku - 1
            keranjang.update(jumlah_buku=newJumlahKeranjang)

            return HttpResponse(b"ADDED", status=201)
        
    return HttpResponseNotFound()

@csrf_exempt
def handle_cart_flutter(request):
    #handle keranjang
    if request.method =='POST':
        data = json.loads(request.body)
        user = int(data["idUser"])
        book = int(data["bookId"])
        action = data["action"]
        if action == "Borrow":
            keranjang = Keranjang.objects.filter(user=user)
            buku = Book.objects.filter(pk = book)
            newStockBuku = buku[0].stock - 1
            buku.update(stock=newStockBuku)
            keranjang[0].book_list.remove(buku[0])
            newJumlahKeranjang = keranjang[0].jumlah_buku - 1
            keranjang.update(jumlah_buku=newJumlahKeranjang)
            #handle peminjaman
            newPeminjaman=Peminjaman(pengguna=user, buku=buku[0], status='dipinjam')
            newPeminjaman.save()
            temp = Peminjaman.objects.filter(pengguna=user, buku=buku[0], status='dipinjam')
            #handle peminjam
            peminjam = Peminjam.objects.filter(user=user)
            peminjam[0].book_list.add(temp[0])
            newJumlahPeminjam = peminjam[0].jumlah_buku_dipinjam + 1
            peminjam.update(jumlah_buku_dipinjam=newJumlahPeminjam)
        
            return JsonResponse({"status": "success"}, status=200)
        elif(action == "Remove") :
            keranjang = Keranjang.objects.filter(user=user)
            buku = Book.objects.filter(pk = book)
            newStockBuku = buku[0].stock + 1
            buku.update(stock=newStockBuku)
            keranjang[0].book_list.remove(buku[0])
            newJumlahKeranjang = keranjang[0].jumlah_buku - 1
            keranjang.update(jumlah_buku=newJumlahKeranjang)

            return JsonResponse({"status": "success"}, status=200)
        
    return JsonResponse({"status": "error"}, status=401)