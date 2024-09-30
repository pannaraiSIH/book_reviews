from django.forms import ModelForm
from .models import Book, Review


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date',
                  'genre', 'description', 'cover_image']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['message', 'rating']
