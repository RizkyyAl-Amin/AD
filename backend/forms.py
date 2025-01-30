from django import forms
from .models import Produk 
from .models import Kategori
from login.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama', 'kategori', 'deskripsi', 'harga']   
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama produk'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Masukkan deskripsi produk',
                'rows': 4
            }),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan harga produk'}),
        }

 
class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ["nama"]  

 

class CreateAkunForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']
