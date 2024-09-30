from django.urls import path
from .views import home, create, update, review, create_review
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('create', create, name='create-book'),
    path('update/<str:pk>/', update, name='update-book'),
    path('review/<str:pk>/', review, name='review-book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
