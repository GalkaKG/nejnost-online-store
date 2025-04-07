from django.shortcuts import render, redirect

from .forms import OrderForm


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from products.models import Cart
from django.contrib.auth.decorators import login_required


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Изпразни количката след поръчката
            if request.user.is_authenticated:
                # Вземи количката на потребителя и изтрий всички елементи
                cart = Cart.objects.get(user=request.user)
                cart.items.all().delete()
                cart.save()
            else:
                # За анонимни потребители, изчисти количката от сесията
                if 'cart' in request.session:
                    del request.session['cart']  # Премахва количката от сесията
                    request.session.modified = True  # Увери се, че сесията е променена

            messages.success(request, "Вашата поръчка беше успешно направена! Количката е изпразнена.")
            return redirect('order_success')
    else:
        form = OrderForm(user=request.user)

    return render(request, 'orders/checkout.html', {'form': form})



def order_success(request):
    return render(request, 'orders/order_success.html')
