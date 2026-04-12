from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import customers_also_bought, register, trending_books
from .views import (
    BookViewSet,
    recommended_books,
    register,
    LoginView,
    view_cart,
    add_to_cart,
    update_cart,
    remove_from_cart,
    view_wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    checkout,
    verify_payment,
    my_orders
)

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/', register),
    path('login/', LoginView.as_view()),

    path('cart/', view_cart),
    path('cart/add/', add_to_cart),
    path('cart/update/<int:item_id>/', update_cart),
    path('cart/remove/<int:item_id>/', remove_from_cart),

    path('wishlist/', view_wishlist),
    path('wishlist/add/', add_to_wishlist),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist),

    path('checkout/', checkout),
    path('verify-payment/', verify_payment),

    path('my-orders/', my_orders),
    path('recommended/', recommended_books, name='recommended'),
    path('also-bought/<int:book_id>/', customers_also_bought),
    path('trending/', trending_books),
]