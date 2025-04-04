from django.urls import path

from .views import product_detail, add_to_cart, view_cart, remove_from_cart, proceed_to_payment

urlpatterns = [
    # path('', product_list, name='product_list'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('payment/', proceed_to_payment, name='proceed_to_payment'),
]
