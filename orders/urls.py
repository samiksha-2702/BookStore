from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('payment-verify/', views.payment_verify, name='payment_verify'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
]