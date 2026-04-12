from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from rest_framework import filters
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend

import razorpay
import hmac
import hashlib

from books.models import Book
from cart.models import Cart, CartItem
from wishlist.models import Wishlist, WishlistItem
from orders.models import Order, OrderItem

from .serializers import (
    BookSerializer,
    RegisterSerializer,
    LoginSerializer,
    CartItemSerializer,
    WishlistSerializer,
    OrderSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter

    search_fields = ['title', 'author', 'category__name']
    ordering_fields = ['price', 'created_at']

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})
    return Response(serializer.errors, status=400)


from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    book_id = request.data.get('book')
    quantity = int(request.data.get('quantity', 1))

    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book_id=book_id
    )

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    item.save()
    return Response({"message": "Item added to cart"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.quantity = int(request.data.get('quantity', 1))
        item.save()
        return Response({"message": "Cart updated"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        return Response({"message": "Item removed"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    serializer = WishlistSerializer(wishlist)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    book_id = request.data.get('book')

    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        book_id=book_id
    )

    return Response({"message": "Added to wishlist"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, item_id):
    try:
        item = WishlistItem.objects.get(id=item_id, wishlist__user=request.user)
        item.delete()
        return Response({"message": "Removed from wishlist"})
    except WishlistItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def checkout(request):
    user = request.user

    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total_amount = 0

    order = Order.objects.create(
        user=user,
        total_amount=0,
        phone=request.data.get("phone", ""),
        status="Pending"
    )

    for item in cart_items:
        price = item.book.price
        quantity = item.quantity

        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=quantity,
            price=price
        )

        total_amount += price * quantity

    order.total_amount = total_amount

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": int(total_amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    order.razorpay_order_id = payment['id']
    order.save()

    return Response({
        "order_id": order.id,
        "razorpay_order_id": payment['id'],
        "amount": total_amount
    })


@api_view(['POST'])
def verify_payment(request):
    razorpay_order_id = request.data.get('razorpay_order_id')
    razorpay_payment_id = request.data.get('razorpay_payment_id')

    try:
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)

        order.razorpay_payment_id = razorpay_payment_id
        order.status = "Completed"
        order.save()

        # clear cart
        CartItem.objects.filter(cart__user=order.user).delete()

        return Response({"message": "Payment successful (test mode)"})

    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

def get_total_amount_calculated(self, obj):
    items = obj.items.all()
    if not items.exists():
        return 0
    return sum(item.quantity * item.price for item in items)