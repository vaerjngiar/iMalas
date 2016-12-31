from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product, Category
from .wishlist import Wishlist
from .forms import WishlistAddProductForm



@require_POST
def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    form = WishlistAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        wishlist.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('wishlist_detail')


def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return redirect('wishlist_detail')


def wishlist_detail(request):
    wishlist = Wishlist(request)
    product_list = Product.objects.all()
    categories = Category.objects.all()
    for item in wishlist:
        item['update_quantity_form'] = WishlistAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})

    context = {'wishlist': wishlist,
               'categories':categories
               }

    return render(request, 'wishlist/wishlist_detail.html', context)


