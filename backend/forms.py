from django import forms
from .models import Produk, GambarProduk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama', 'kategori', 'harga']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama produk'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'harga': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan harga produk'}),
        }

 