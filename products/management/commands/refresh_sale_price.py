from django.core.management.base import BaseCommand, CommandError

from products.models import Product


class Command(BaseCommand):
    help = 'Refreshes all product prices'

    def add_arguments(self, parser):
        parser.add_argument('--percent', type=float)

    def handle(self, *args, **options):
        return Product.objects.refresh_sale_price(percent=options['percent'])