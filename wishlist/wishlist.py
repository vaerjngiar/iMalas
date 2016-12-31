from decimal import Decimal
from django.conf import settings
from products.models import Product


class Wishlist(object):
    
    def __init__(self, request):
        self.session = request.session
        whishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not whishlist:
            whishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.whishlist = whishlist

    def __len__(self):
        return sum(item['quantity'] for item in self.whishlist.values())

    def __iter__(self):
        product_ids = self.whishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.whishlist[str(product.id)]['product'] = product

        for item in self.whishlist.values():
            item['sale_price'] = Decimal(item['sale_price'])
            item['total_price'] = item['sale_price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.whishlist:
            self.whishlist[product_id] = {'quantity': 0,
                                          'sale_price': str(product.sale_price)
                                          }
        if update_quantity:
            self.whishlist[product_id]['quantity'] = quantity
        else:
            self.whishlist[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.whishlist:
            del self.whishlist[product_id]
            self.save()

    def save(self):
        self.session[settings.WISHLIST_SESSION_ID] = self.whishlist
        self.session.modified = True

    def clear(self):
        self.session[settings.WISHLIST_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['sale_price']) * item['quantity'] for item in self.whishlist.values())