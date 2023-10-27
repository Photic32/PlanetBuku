from django.shortcuts import render
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from book.models import Book
from home.models import Peminjaman, Keranjang
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


def show_home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_staff == True:
            context = {
                'last_login': request.COOKIES['last_login'],
                'username' : user.username,
            }

            return render(request, "homeAdmin.html", context)
        else:
            context = {
                'last_login': request.COOKIES['last_login'],
                'username' : user.username,
            }

            return render(request, "homeUser.html", context)
    else:
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
