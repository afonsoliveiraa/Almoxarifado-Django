from django.db import models
from django.utils import timezone


# Create your models here.


class Produto(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    estoque = models.PositiveIntegerField(default=0)
    data = models.DateField(default=timezone.now)
    data_anterior = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Entrada(models.Model):
    number = models.CharField(max_length=255)
    date_create = models.DateField()
    supplier = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.date_create} - {self.total}'


class Item_Entrada(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.PROTECT, related_name='entrada_item')
    produto_entrada = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='produto_item')
    amount_produto = models.PositiveIntegerField()
    price_produto = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.produto_entrada} da entrada {self.entrada}'


class Saida(models.Model):
    destiny = models.CharField(max_length=255)
    date_create = models.DateField()
    requester = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.date_create} - {self.requester}'


class Item_Saida(models.Model):
    saida = models.ForeignKey(Saida, on_delete=models.PROTECT, related_name='saida_item')
    produto_saida = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='produto_saida')
    amount_produto = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.produto_saida} da saida {self.saida}'
