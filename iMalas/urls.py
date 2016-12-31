"""iMalas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from carts.views import CartView, ItemCountView, CheckoutView, CheckoutFinalView, TotalSumView
from orders.views import (
                    AddressSelectFormView,
                    UserAddressCreateView,
                    OrderList,
                    OrderDetail)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.urls_categories')),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^cart/total/$', TotalSumView.as_view(), name='total_sum'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
    url(r'^wishlist/', include('wishlist.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^about/', include('about.urls')),
    url(r'^', include('home.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
