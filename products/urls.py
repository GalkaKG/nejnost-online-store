from django.urls import path

from .views import product_detail, proceed_to_payment

urlpatterns = [
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('payment/', proceed_to_payment, name='proceed_to_payment'),
]
