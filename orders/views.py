from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

import razorpay
import json
import hmac
import hashlib

from cart.models import Cart, CartItem
from .models import Order, OrderItem

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def checkout(request):
    """Checkout page: shows cart and lets user proceed to payment"""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('view_cart')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return redirect('view_cart')

    # Calculate total and per-item total
    total_amount = 0
    for item in cart_items:
        item.total_price = item.book.price * item.quantity
        total_amount += item.total_price

    if request.method == "POST":
        # Create Django order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status="Pending"
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        # Redirect to payment page with order ID
        return redirect('payment', order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount
    })


@login_required
def payment_view(request, order_id):
    """Payment page: creates Razorpay order and opens checkout"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_items = order.items.all()

    
    if order.razorpay_order_id:
        razorpay_order_id = order.razorpay_order_id
    else:
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": int(order.total_amount * 100),  # paise
            "currency": "INR",
            "payment_capture": 1
        })
        razorpay_order_id = razorpay_order['id']
        order.razorpay_order_id = razorpay_order_id
        order.save()

    context = {
        "total_amount": order.total_amount,
        "razorpay_amount": int(order.total_amount * 100),
        "razorpay_order_id": razorpay_order_id,
        "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        "order": order,
        "cart_items": cart_items
    }

    return render(request, "orders/payment.html", context)


@csrf_exempt
@login_required
def payment_verify(request):
    """Verify Razorpay payment signature"""
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        # Verify signature
        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
            msg=bytes(f"{razorpay_order_id}|{razorpay_payment_id}", 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            # Payment verified
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id, user=request.user)
            order.status = "Completed"
            order.razorpay_payment_id = razorpay_payment_id
            order.save()
            return JsonResponse({"status": "success", "order_id": order.id})

        return JsonResponse({"status": "fail"})
    return JsonResponse({"status": "invalid method"})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Pre-calculate total price per item
    for item in order.items.all():
        item.total_price = item.price * item.quantity

    return render(request, "orders/order_success.html", {"order": order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Add total_price for each item
    for item in order.items.all():
        item.total_price = item.price * item.quantity

    # Render invoice to PDF
    html = render_to_string('orders/invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response