from django.contrib import messages
from django.shortcuts import render, redirect

from products.models import Cart
# from django.contrib.auth.decorators import login_optional
from .forms import OrderForm
from .models import OrderItem


def checkout_view(request):
    # Получаваме количката в началото, за да я използваме и при GET и при POST заявки
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).prefetch_related('items__variant').first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key, user=None).prefetch_related('items__variant').first()

    # Ако няма количка или количката е празна
    if not cart or not cart.items.exists():
        messages.error(request, "Вашата количка е празна или не съществува.")
        return redirect('view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                # Създаване на поръчката
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                order.save()

                # Създаване на артикулите в поръчката
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        variant=item.variant,
                        quantity=item.quantity,
                        price=item.variant.get_final_price()  # Добавете цената, ако е необходимо
                    )

                # Изчистване на количката след успешна поръчка
                cart.items.all().delete()
                cart.delete()  # Изтриваме самата количка

                messages.success(request, "Вашата поръчка беше успешно направена!")
                return redirect('order_success', order_id=order.id)

            except Exception as e:
                messages.error(request, f"Възникна грешка при обработката на поръчката: {str(e)}")
                return redirect('checkout')
    else:
        # Попълване на формата с първоначални данни
        initial_data = {}
        if request.user.is_authenticated:
            initial_data.update({
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            })
        form = OrderForm(user=request.user, initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': sum(item.get_total_price() for item in cart.items.all())
    }
    return render(request, 'orders/order_success.html', context)


def order_success(request):
    return render(request, 'orders/order_success.html')
