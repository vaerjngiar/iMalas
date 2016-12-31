from django.test import TestCase
from products.models import Product
from django.core.urlresolvers import reverse


class ProductModelTestsCase(TestCase):
    """Product model tests."""

    def SetUp(self):
        Product.objects.create(title='A new Product', price=1.20, sale_price=1.00)

    def create_product(self, title='Some product', price=2.40, sale_price=2.00):
        return Product.objects.create(title=title, price=price, sale_price=sale_price)

    def test_str(self):
        product = Product(title='Notebook')
        self.assertEquals(str(product), 'Notebook')


class ProductViewTestsCase(TestCase):
    """Product view tests"""

    def create_product(self, title='Some product', price=3.60, sale_price=3.00):
        return Product.objects.create(title=title, price=price, sale_price=sale_price)

    def test_list_view(self):
        list_url = reverse("products")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        obj = self.create_product(title='Another Product Test',price=4.80, sale_price=4.00)
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code, 200)

