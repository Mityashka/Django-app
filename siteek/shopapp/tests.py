from string import ascii_letters
from random import choices
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from shopapp.models import Product
from shopapp.utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin1')
        self.client.login(username='admin', password='admin1')
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:create_product'),
            {
                'name': self.product_name,
                'price': '100',
                'description': 'Test description',
                'discount': '5',
            }, HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.product = Product.objects.create(name='Best Product')

    @classmethod
    def tearDown(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:products_details', kwargs={'pk': self.product.pk}), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_product(self):
        response = self.client.get(
            reverse('shopapp:products_details', kwargs={'pk': self.product.pk}), HTTP_USER_AGENT='test-agent')
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = ['products-fixture.json']

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'), HTTP_USER_AGENT='test-agent')
        products = Product.objects.filter(archived=False).all()
        products_ = response.context['products']
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='admin', password='admin1')
        cls.user = User.objects.create_superuser(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='test-agent')
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = ['products-fixture.json']

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products-export'), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data['products'], expected_data)
