from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from home.models import Keranjang
from daftar_peminjam.models import Peminjam
from django.urls import reverse


@csrf_exempt
def register(request):
    form = UserCreationForm()
    if request.method == "POST": 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            newKeranjang = Keranjang(user=user)
            newKeranjang.save()
            newPeminjam = Peminjam(user=user)
            newPeminjam.save()
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Signup User sukses!",
                "user_id": user.pk,
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Signup gagal, mohon cek lagi."
            }, status=401)


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # Status login sukses.
            if(user.is_staff == True):
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login Admin sukses!",
                    "is_staff":True,
                    "staff_id":user.pk,
                    "user": {"id": user.pk,
                             "password": user.password,
                             "last_login": user.last_login,
                             "is_superuser": user.is_superuser,
                             "username": user.username,
                             "last_name": user.last_name,
                             "email": user.email,
                             "is_staff": user.is_staff,
                             "is_active": user.is_active,
                             "date_joined": user.date_joined,
                             "first_name": user.first_name,
                    }
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                }, status=200)
            else:
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login User sukses!",
                    "is_staff": False,
                    "user_id": user.pk,
                    "user": {"id": user.pk,
                             "password": user.password,
                             "last_login": user.last_login,
                             "is_superuser": user.is_superuser,
                             "username": user.username,
                             "last_name": user.last_name,
                             "email": user.email,
                             "is_staff": user.is_staff,
                             "is_active": user.is_active,
                             "date_joined": user.date_joined,
                             "first_name": user.first_name,
                    }
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def logout(request):
    print(request.user.username)
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
#@login_required(login_url='/accounts/login/')
def tes(request):
    try:
        return JsonResponse({
            "status": True,
            "message": "YAYYYYY!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
