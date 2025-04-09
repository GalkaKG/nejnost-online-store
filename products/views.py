from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Product, ProductVariant
from cart.models import Cart


# @cache_page(60 * 15)  # Кеширане за 15 минути
def product_list(request):
    # Взимаме параметъра за сортиране от URL
    sort_by = request.GET.get('sort', '')  # Празно по подразбиране

    # Взимаме всички продукти
    products = Product.objects.prefetch_related('variants__color').all()

    # Прилагаме сортиране според избраната опция
    if sort_by == 'price_asc':
        products = products.order_by('base_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-base_price')
    elif sort_by == 'updated':
        products = products.order_by('-id')  # Или '-updated_at' ако имате такова поле
    else:
        # По подразбиране - първи създадени (рандом)
        products = products.order_by('?')

    return render(request, 'products/product_list.html', {
        'products': products,
        'current_sort': sort_by
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = product.variants.all()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants
    })





def proceed_to_payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    if not cart_items:
        messages.warning(request, "Вашата количка е празна.")
        return redirect('product_list')

    return render(request, 'payments/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
