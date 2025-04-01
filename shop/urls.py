from django.contrib import admin
from django.urls import path, include
from products.views import product_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', product_list, name='home'),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
]
