from django.urls import include, path
from .views import book_list, book_detail, bestsellers

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/', book_list, name='book_list_alt'),
    path('bestsellers/', bestsellers, name='bestsellers'),
    path('book/<int:id>/', book_detail, name='book_detail'),
]