from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Product, ProductVariant, Cart, CartItem


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
        # По подразбиране - първи създадени (най-стари)
        products = products.order_by('id')

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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')

    if not variant_id:
        messages.error(request, "Моля изберете вариант.")
        return redirect('product_detail', product_id=product.id)

    try:
        variant = ProductVariant.objects.get(id=variant_id, product=product)
    except ProductVariant.DoesNotExist:
        messages.error(request, "Невалиден избор на вариант.")
        return redirect('product_detail', product_id=product.id)

    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(
        request,
        f"Продуктът {product.name} ({variant.color.name}) беше добавен в количката."
    )
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if 1 <= quantity <= 10:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Количеството беше обновено.")
            else:
                messages.error(request, "Моля изберете количество между 1 и 10.")
        except ValueError:
            messages.error(request, "Невалидно количество.")
    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user
    )
    product_name = cart_item.variant.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} беше премахнат от количката.")
    return redirect('view_cart')


@login_required
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
