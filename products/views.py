# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
#
# from .models import Product, Cart
#
#
# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'products/product_list.html', {'products': products})
#
#
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'products/product_detail.html', {'product': product})
#
#
# # Add to cart view
# @login_required
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     color = request.POST.get('color')
#
#     # Проверяваме дали цветът е валиден
#     if not color in dict(Product.COLORS):
#         messages.error(request, "Невалиден избор на цвят.")
#         return redirect('product_detail', product_id=product.id)
#
#     # Добавяме продукта в количката с избрания цвят
#     cart = request.session.get('cart', [])
#     cart.append({
#         'product_id': product.id,
#         'color': color,
#         'quantity': 1,  # може да се промени, ако има опция за избор на количество
#     })
#     request.session['cart'] = cart
#     messages.success(request, f"Продуктът {product.name} с цвят {color} беше добавен в количката.")
#     return redirect('product_list')
#
#
# # View for showing cart items
# @login_required
# def view_cart(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_price = sum(item.total_price() for item in cart_items)
#     return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})
#
#
# # Remove item from cart
# @login_required
# def remove_from_cart(request, cart_item_id):
#     cart_item = Cart.objects.get(id=cart_item_id)
#     cart_item.delete()
#     return redirect('view_cart')
#
#
# # Proceed to payment
# @login_required
# def proceed_to_payment(request):
#     # For now, just display the total price
#     cart_items = Cart.objects.filter(user=request.user)
#     total_price = sum(item.total_price() for item in cart_items)
#     return render(request, 'payments/payment.html', {'total_price': total_price})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, ProductVariant, Cart, CartItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


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