from django.db import models

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nama


class Produk(models.Model):
    no_produk = models.CharField(max_length=20, unique=True, editable=False)
    nama = models.CharField(max_length=100)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name="produk")
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.IntegerField()  

    def save(self, *args, **kwargs):
        if not self.no_produk:
            total_produk = Produk.objects.count() + 1
            self.no_produk = f'PRD-{total_produk:05}'  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama



class GambarProduk(models.Model):
    def upload_to_products(instance, filename):
        return f'products/{filename}'

    path_gambar = models.ImageField(upload_to=upload_to_products)
    no_produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='gambar_produk')

    def __str__(self):
        return f"Gambar untuk {self.no_produk.nama}"
