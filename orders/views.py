from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
import requests


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Възможна интеграция с API на Speedy или Econt
            courier = order.courier
            if courier == 'Speedy':
                # Изпращаме заявка до Speedy API
                response = requests.post('https://api.speedy.bg/v1/shipment', data={...})
            elif courier == 'Econt':
                # Изпращаме заявка до Econt API
                response = requests.post('https://www.econt.com/api/', data={...})

            # Връщаме се към потребителя
            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


def order_success(request):
    return render(request, 'orders/order_success.html')
