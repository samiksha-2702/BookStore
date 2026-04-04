from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .models import Order, OrderItem


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')

    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('view_cart')

    total = 0
    for item in items:
        total += item.book.price * item.quantity

    # 🧾 Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    # 📦 Create Order Items
    for item in items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

    # 🧹 Clear Cart
    items.delete()

    return render(request, 'orders/order_success.html', {'order': order})