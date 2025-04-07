from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order
import requests


def checkout_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('thank_you')
    else:
        form = OrderForm(user=request.user)
    return render(request, 'orders/checkout.html', {'form': form})


def order_success(request):
    return render(request, 'orders/order_success.html')



