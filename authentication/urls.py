from django.urls import path
from authentication.views import login, logout, tes, register

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('tes/', tes, name='tes'),
    path('register/', register, name='register')

]