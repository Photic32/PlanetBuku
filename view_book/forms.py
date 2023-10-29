from django.forms import ModelForm
from view_book.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review", "rate"]
        labels = {
            "review": "Review", 
            "rate": "Rate (0-5)",  
        }
        