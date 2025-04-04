from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Cart


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# Add to cart view
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if item is already in the cart
        cart_item.save()

    return redirect('view_cart')


# View for showing cart items
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Remove item from cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


# Proceed to payment
@login_required
def proceed_to_payment(request):
    # For now, just display the total price
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'payment.html', {'total_price': total_price})
