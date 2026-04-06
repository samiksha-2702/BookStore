from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]