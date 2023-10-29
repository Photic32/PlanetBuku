from django.forms import ModelForm
from .models import Peminjam, Peminjaman

class PeminjamanForm(ModelForm):
    class Meta:
        model = Peminjaman
        fields = ["tanggal_pengembalian"]

class KembaliForm(ModelForm):
    class Meta:
        model = Peminjaman
        fields = ["status"]
