from django.urls import path
from authentication.views import login, logout, tes

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('tes/', tes, name='tes'),
]