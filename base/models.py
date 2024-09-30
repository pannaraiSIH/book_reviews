from django.db import models
from django.contrib.auth.models import User
from static.base.constants import GENRE_CHOICES

# Create your models here.


# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField()
#     created = models.DateTimeField(auto_now=True)
#     updated = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    create_user = models.ForeignKey(
        User, related_name='books_created', on_delete=models.CASCADE, null=True)
    update_user = models.ForeignKey(
        User, related_name='books_updated', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    message = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    book = models.ForeignKey(
        Book, related_name='book_reviewed', on_delete=models.DO_NOTHING, null=True)
    create_user = models.ForeignKey(
        User, related_name='review_created', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)
