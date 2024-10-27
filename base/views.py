from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import BookForm, ReviewForm
from .models import Book, Review
from django.contrib.auth.models import User
from django.db.models import Avg, Q
from static.base.constants import GENRE_CHOICES
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    search = request.GET.get('search') if request.GET.get(
        'search') != None else ''

    books = Book.objects.filter(
        Q(genre__icontains=search) | Q(title__icontains=search))
    book_count = books.count()

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("get:", request.GET)
    print(page_obj)

    context = {'books': books, 'book_count': book_count, 'rating_list': range(
        5), 'genres': GENRE_CHOICES, 'page_obj': page_obj}

    return render(request, 'base/book_list.html', context)


@login_required(login_url='login')
def create(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.create_user = request.user
            form.save()
            return redirect('home')

    return render(request, 'base/book_form.html', {'form': form})


@login_required(login_url='login')
def update(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            book = form.save(commit=False)
            book.create_user = request.user
            book.save()
            return redirect('home')

    return render(request, 'base/book_form.html', {'form': form})


@login_required(login_url='login')
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


@login_required(login_url='login')
def review(request, pk):
    book = Book.objects.get(id=pk)
    reviews = Review.objects.filter(book=book)

    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.create_user = request.user
            review.save()
            update_average_rating(book=book)

    context = {'book': book, 'reviews': reviews, 'rating_list': range(5)}
    return render(request, 'base/review.html', context)


@login_required(login_url='login')
def create_review(request):
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()

    return render(request, 'base/review.html')


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username or password does not exist')
            return render(request, 'base/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    return render(request, 'base/login.html', {'page': page})


def logout_page(request):
    logout(request)
    return redirect('home')


def register_user(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occur during registration')

    return render(request, 'base/login.html', {'page': page, 'form': form})
