from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from products.models import Product, ProductVariant


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

    # За автентифицирани потребители
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # За анонимни потребители
        if not request.session.session_key:
            request.session.create()  # Ensure session exists
        session_key = request.session.session_key

        # Търсим колички с този session_key
        carts = Cart.objects.filter(session_key=session_key)

        # Ако има повече от една количка, вземаме първата
        if carts.exists():
            cart = carts.first()  # Вземаме първата количка (можеш да добавиш допълнителна логика за избор)
        else:
            # Ако няма количка, създаваме нова
            cart = Cart.objects.create(session_key=session_key, user=None)  # Добави user=None за неавтентифицираните
            request.session.save()  # Записваме сесията, ако е създадена нова количка за анонимен потребител

    # Добави или обнови продукта в количката
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Съобщение за успешно добавяне
    messages.success(
        request,
        f"Продуктът {product.name} ({variant.color.name}) беше добавен в количката."
    )

    # Пренасочване към страницата с количката
    return redirect('view_cart')


def view_cart(request):
    if request.user.is_authenticated:
        # Get the cart for authenticated users
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = None
    else:
        # For guest users, get the cart using the session key
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if not cart:
            messages.info(request, "Във вашата количка няма продукти.")

    if cart:
        cart_items = cart.items.all()
        total_price = sum(item.get_total_price() for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def update_cart_item(request, item_id):
    if request.method == 'POST':
        # For authenticated users, use user-specific cart items
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        else:
            # For anonymous users, use session-based cart items
            cart_item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key)

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


def remove_from_cart(request, cart_item_id):
    # For authenticated users, use user-specific cart items
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    else:
        # For anonymous users, use session-based cart items
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__session_key=request.session.session_key)

    product_name = cart_item.variant.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} беше премахнат от количката.")
    return redirect('view_cart')
