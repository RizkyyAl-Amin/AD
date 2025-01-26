from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produk/<str:no_produk>/', views.product_details, name='product_details'),
]
