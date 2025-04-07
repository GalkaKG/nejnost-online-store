from django.urls import path
from .views import checkout_view, order_success

urlpatterns = [
    path('checkout/', checkout_view, name='checkout',),
    path('success/', order_success, name='order_success'),
    # path("thankyou/", )
    # path('payment/', payment_view, name='payment'),
    # path('payment/success/', success_view, name='success_url'),
    # path('payment/error/', error_view, name='error_url'),
]
