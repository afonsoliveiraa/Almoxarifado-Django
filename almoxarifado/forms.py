from django import forms

from almoxarifado.models import Produto, Entrada, Item_Entrada, Saida, Item_Saida


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['estoque', 'data', 'data_anterior']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class Item_EntradaForm(forms.ModelForm):
    class Meta:
        model = Item_Entrada
        exclude = ['entrada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class Item_SaidaForm(forms.ModelForm):
    class Meta:
        model = Item_Saida
        exclude = ['saida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})