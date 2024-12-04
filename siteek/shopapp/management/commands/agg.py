from itertools import product, count
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from django.db import transaction
from django.db.models import Avg, Min, Max, Count, Sum

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        # result = Product.objects.filter(
        #     name__contains='smartphone').aggregate(
        #     Avg('price'),
        #     Max('price'),
        #     min_price = Min('price'),
        #     count = Count('id'),
        # )
        # print(result)
        orders = Order.objects.annotate(
            total = Sum('products__price', default=0),
            products_count = Count('products'),
        )
        for order in orders:
            print(f'Order #{order.id}'
                  f'with total {order.products_count} '
                  f'products worth {order.total}')
        self.stdout.write('Done')