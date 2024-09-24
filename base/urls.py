from django.urls import path
from .views import home, create, update

urlpatterns = [
    path('', home, name='home'),
    path('create', create, name='create-book'),
    path('update/<str:pk>/', update, name='update-book')
]
