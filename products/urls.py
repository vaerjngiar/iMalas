from django.conf.urls import url
from .views import ProductListView, ProductDetailView, VariationListView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='products'),
    #url(r'^(?P<category_slug>[-\w]+)/$', ProductListView.as_view(), name='product_list_by_category'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
]