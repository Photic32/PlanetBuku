from django.forms import ModelForm
from borrowed_book_list.models import KesanPeminjam

class KesanPeminjamForm(ModelForm):
    class Meta:
        model = KesanPeminjam
        fields = ["kesan"]