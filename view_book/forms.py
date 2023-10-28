from django.forms import ModelForm
from view_book.models import Review

class RewiewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review", "rate"]