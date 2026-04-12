from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from books.models import Book, Category
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from wishlist.models import Wishlist, WishlistItem
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', 'address_line1', 'address_line2', 'city', 'state', 'pincode']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)

        profile = user.profile
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()

        return user


class LoginSerializer(TokenObtainPairSerializer):
    pass


class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_title', 'book_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.book.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cart_price']

    def get_total_cart_price(self, obj):
        return sum(item.quantity * item.book.price for item in obj.cartitem_set.all())


class WishlistItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'book', 'book_title', 'added_at']


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(source='wishlistitem_set', many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'items']


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount_calculated = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'total_amount',
            'status',
            'phone',
            'created_at',
            'razorpay_order_id',
            'razorpay_payment_id',
            'items',
            'total_amount_calculated'
        ]

    def get_total_amount_calculated(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())