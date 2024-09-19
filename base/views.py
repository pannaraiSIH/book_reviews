from django.shortcuts import render
from static.base.constants import image

# Create your views here.


def home(request):
    context = {'books': range(15), 'rating_list': range(5), 'image': image}
    return render(request, 'base/book_list.html', context)


def create(request):
    return render(request, 'base/create_book.html')
