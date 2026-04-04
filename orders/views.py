from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import CartItem
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from cart.models import CartItem, Cart

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []

    # Calculate total for each item and overall total
    total_amount = 0
    for item in cart_items:
        item.total_price = item.book.price * item.quantity
        total_amount += item.total_price

    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status='Completed'
        )
        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        # Clear cart
        cart_items.delete()
        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

# Order success page
@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})

# Order history page
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

@login_required
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    html = render_to_string('orders/invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Add total_price for each item
    for item in order.items.all():  # related_name='items'
        item.total_price = item.price * item.quantity

    return render(request, 'orders/invoice.html', {'order': order})