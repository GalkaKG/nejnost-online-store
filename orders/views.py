from django.contrib import messages
from django.shortcuts import render, redirect

from products.models import Cart
from .forms import OrderForm
from .models import OrderItem


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Get cart for authenticated or anonymous user
            if request.user.is_authenticated:
                cart = Cart.objects.filter(user=request.user).first()
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.save()
                    session_key = request.session.session_key
                cart = Cart.objects.filter(session_key=session_key).first()

            print("🛒 Cart items:", cart.items.all())  # DEBUG
            if cart:
                for item in cart.items.all():
                    try:
                        OrderItem.objects.create(
                            order=order,
                            variant=item.variant,
                            quantity=item.quantity
                        )
                    except Exception as e:
                        print("⚠️ Грешка при създаване на OrderItem:", e)
                cart.items.all().delete()
                cart.save()

            messages.success(request, "Вашата поръчка беше успешно направена! Количката е изпразнена.")
            return redirect('order_success')
    else:
        form = OrderForm(user=request.user)

    return render(request, 'orders/checkout.html', {'form': form})


def order_success(request):
    return render(request, 'orders/order_success.html')
