from django.shortcuts import redirect, render
from .models import Cart, CartItem
from books.models import Book

def add_to_cart(request, book_id):
    user = request.user

    # get or create cart
    cart, created = Cart.objects.get_or_create(user=user)

    book = Book.objects.get(id=book_id)

    # check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('book_list')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = 0
    for item in items:
        total += item.book.price * item.quantity

    return render(request, 'cart/cart.html', {
        'cart_items': items,
        'total': total
    })