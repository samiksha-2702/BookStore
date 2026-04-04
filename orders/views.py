from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import CartItem
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# Checkout page
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Simulate payment success
        order = Order.objects.create(user=request.user, total_amount=total, status='Completed')

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

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})

# Order success page
@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/success.html', {'order': order})

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