from itertools import product

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')
        """
        Update
        """
        result = Product.objects.filter(name__contains='smartphone').update(discount=10)

        print(result)




        # info = [
        #     ('smartphone 1', 199),
        #     ('smartphone 2', 299),
        #     ('smartphone 3', 399),
        # ]
        # prodicts = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(prodicts)
        #
        # for obj in result:
        #     print(obj)
        self.stdout.write(f'Done')
