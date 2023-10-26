from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from borrowed_book_list.models import Peminjaman

@login_required
def borrowed_book_list(request):
    peminjaman_dipinjam = Peminjaman.objects.filter(user=request.user, status =('dipinjam', 'Dipinjam'))
    peminjaman_dikembalikan = Peminjaman.objects.filter(user = request.user, status = ('dikembalikan', 'Dikembalikan'))
    context = {
        'peminjaman_dipinjam' : peminjaman_dipinjam,
        'peminjaman_dikembalikan' : peminjaman_dikembalikan,
    }

    return render(request, "borrowed_book_list.html", context)
# Create your views here.
