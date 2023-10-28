from django.db import models
from book.models import Book
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    rate = models.IntegerField(default=0)
    review_date = models.DateField(auto_now_add=True)