from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from books.models import Book

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from xhtml2pdf import pisa

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    total_amount = sum(item.book.price * item.quantity for item in cart_items)

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        "amount": int(total_amount * 100),  # amount in paise
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save order in DB with status 'Pending'
    order = Order.objects.create(user=user, total_amount=total_amount, status="Pending")
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )
    
    # Do not clear cart yet – wait until payment success

    context = {
        "order": order,
        "razorpay_order_id": razorpay_order['id'],
        "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        "total_amount": total_amount,
    }
    return render(request, 'orders/payment.html', context)

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


    for item in order.items.all(): 
        item.total_price = item.price * item.quantity

    return render(request, 'orders/invoice.html', {'order': order})


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # You receive Razorpay payment_id and order_id
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        order_id = data.get("order_id")  # your DB order_id

        # Mark the order as completed
        order = Order.objects.get(id=order_id)
        order.status = "Completed"
        order.save()

        # Clear user's cart
        CartItem.objects.filter(cart__user=order.user).delete()

        return redirect('order_success', order_id=order.id)