from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ShopIndexView, GroupsListView, ProductsListView, OrdersListView, ProductDetailsView, OrderDetailsView,
                    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductsDataExportView, ProductViewSet)
app_name = 'shopapp'
routers = DefaultRouter()
routers.register("products", ProductViewSet)
urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path("api/", include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/export', ProductsDataExportView.as_view(), name='products-export'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_details'),
]
