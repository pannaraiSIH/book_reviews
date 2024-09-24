from django.shortcuts import render, HttpResponseRedirect, redirect
from static.base.constants import image
from .forms import BookForm
from .models import Book
from django.contrib import messages

# Create your views here.


def home(request):
    search = None
    books = Book.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search')

        if search:
            books = Book.objects.filter(title__icontains=search)
    context = {'books': books, 'rating_list': range(
        5), 'image': image}
    return render(request, 'base/book_list.html', context)


def create(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)

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
