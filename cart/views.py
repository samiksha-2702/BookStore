from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from books.models import Book


#  View Cart
def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/') # temporary (we'll fix with login later)

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = 0
    for item in items:
        item.total = item.book.price * item.quantity
        total += item.total

    return render(request, 'cart/cart.html', {
        'cart_items': items,
        'total': total
    })


#  Add to Cart
def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')  # temporary

    cart, created = Cart.objects.get_or_create(user=request.user)
    book = Book.objects.get(id=book_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


# Remove Item
def remove_from_cart(request, item_id):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)
    
    # Get the cart item in that cart
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Delete the item
    item.delete()
    
    return redirect('view_cart')


# Increase Quantity
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


#  Decrease Quantity
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('view_cart')