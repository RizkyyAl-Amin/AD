from django.urls import path
from . import views

urlpatterns = [
    path('produk/', views.list_produk, name='list_produk'),  
    path('produk/create/', views.create_produk, name='create_produk'),  
    path('produk/update/<int:produk_id>/', views.update_produk, name='update_produk'),
    path('delete_produk/<int:pk>/', views.delete_produk, name='delete_produk'),
    path('produk/<str:no_produk>/gambar/', views.tampilkan_gambar_produk, name='tampilkan_gambar_produk'),
]
