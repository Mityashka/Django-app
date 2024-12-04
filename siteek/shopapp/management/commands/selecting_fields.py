from itertools import product
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from typing import Sequence
from django.db import transaction
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        user_info = User.objects.values_list('username', flat=True)
        print(user_info)
        for user in user_info:
            print(user)

        products_values = Product.objects.values('pk', 'name')
        for p_values in products_values:
            print(p_values)

        self.stdout.write('Done')
