from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import BookForm, ReviewForm
from .models import Book, Review
from django.db.models import Avg, Q
from static.base.constants import GENRE_CHOICES

# Create your views here.


def home(request):
    search = request.GET.get('search') if request.GET.get(
        'search') != None else ''

    books = Book.objects.filter(
        Q(genre__icontains=search) | Q(title__icontains=search))
    book_count = books.count()

    context = {'books': books, 'book_count': book_count, 'rating_list': range(
        5), 'genres': GENRE_CHOICES}

    return render(request, 'base/book_list.html', context)


def create(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/book_form.html', {'form': form})


def update(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/book_form.html', {'form': form})


def delete(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('home')


def update_average_rating(book):
    reviews = Review.objects.filter(book=book)
    if reviews.exists():
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        print("average_rating", average_rating)
        book.average_rating = average_rating
        book.save()


def review(request, pk):
    book = Book.objects.get(id=pk)
    reviews = Review.objects.filter(book=book)

    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            update_average_rating(book=book)

    context = {'book': book, 'reviews': reviews, 'rating_list': range(5)}
    return render(request, 'base/review.html', context)


def create_review(request):
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()

    return render(request, 'base/review.html')
