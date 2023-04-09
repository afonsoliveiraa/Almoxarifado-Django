from django.contrib.auth import forms
from django.contrib import admin
from django.contrib.auth.models import User

from almoxarifado.models import Produto, Entrada, Item_Entrada, Saida, Item_Saida

# Register your models here.


admin.site.register(Produto)

admin.site.register(Entrada)

admin.site.register(Item_Entrada)

admin.site.register(Saida)

admin.site.register(Item_Saida)


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
