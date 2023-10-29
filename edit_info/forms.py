from django.forms import ModelForm, TextInput
from edit_info.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["isbn", "title", "author", "publication_year", "publisher", "image_s", "image_m", "image_l", "stock"]
        widgets = {
            "isbn": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "title": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "author": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "publisher": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "publication_year": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "image_s": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "image_m": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
            "image_l": TextInput(attrs={'class': 'your-css-class', 'size': 40}),
        }