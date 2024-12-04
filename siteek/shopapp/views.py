"""
В этом модуле лежат различные наборы представления для интернет-магазина.

Разные view интернет магазина.
"""
import csv
from crypt import methods
from csv import DictWriter
from dataclasses import fields
from itertools import product
from lib2to3.fixes.fix_input import context
from timeit import default_timer
import logging
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action, parser_classes
from django.contrib.admin import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from .models import Product, Order, ProductImage
from .forms import ProductForm
from django.views import View
from .forms import GroupForm
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.reverse import reverse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .common import save_csv_products

log = logging.getLogger(__name__)


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        print('Hello products list')
        return super().list(*args, **kwargs)

    @action(detail=False, methods=['get'])
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow(
                {
                    field: getattr(product, field)
                    for field in fields
                }
            )
        return response

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(summary='Get one product by id',
                   description='Retrieves **product**, return 404 if not found',
                   responses={
                       200: ProductSerializer,
                       404: OpenApiResponse(description='Empty response, product not found')})
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class ShopIndexView(View):

    def get(self, request: HttpRequest):
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 5
        }
        log.debug('Products for shop index: %s', product)
        log.info('Rendering shop index')
        print('shop index context', context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest):
        context = {
            'form': GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('shopapp:products_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        # .select_related('user').
        # prefetch_related('products')
        .all()
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class ProductsDataExportView(View):
    def get(self, request: HttpRequest):
        cache_key = 'products-data-export'
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
            elem = products_data[0]
            name = elem['name']
            print("name: ", name)
        return JsonResponse({'products': products_data})
