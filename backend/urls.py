from django.urls import path
from . import views

urlpatterns = [
    path('produk', views.list_produk, name='list_produk'),  
    path('produk/create/', views.create_produk, name='create_produk'),  
    path('produk/update/<int:produk_id>/', views.update_produk, name='update_produk'),
    path('delete_produk/<int:pk>/', views.delete_produk, name='delete_produk'),
    path('produk/<str:no_produk>/gambar/', views.tampilkan_gambar_produk, name='tampilkan_gambar_produk'),
    path('kategori', views.list_kategori, name="list_kategori"),
    path("kategori/tambah/", views.create_kategori, name="create_kategori"),
    path("kategori/edit/<int:kategori_id>/", views.update_kategori, name="update_kategori"),
    path("akun", views.list_akun, name="list_akun"),
    path("akun/create/", views.create_akun, name="create_akun"),
    path("akun/delete/<int:user_id>/", views.delete_akun, name="delete_akun"),
    path("kategori/delete/<int:kategori_id>/", views.delete_kategori, name="delete_kategori"), 
]
