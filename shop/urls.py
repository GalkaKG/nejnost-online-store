from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from products.views import product_list

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', product_list, name='home'),
                  path('products/', include('products.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('orders/', include('orders.urls')),
                  path('orders/', include('orders.urls')),
                  path('core/', include('core.urls')),
                  path('cart/', include('cart.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
