# Generated by Django 5.1.3 on 2025-01-25 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_produk', models.CharField(max_length=20, unique=True)),
                ('nama', models.CharField(max_length=100)),
                ('kategori', models.CharField(max_length=50)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='no_produk',
        ),
        migrations.CreateModel(
            name='GambarProduk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path_gambar', models.ImageField(upload_to='produk_gambar/')),
                ('no_produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gambar_produk', to='backend.produk')),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
