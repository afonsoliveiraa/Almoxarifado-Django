# Generated by Django 4.2 on 2023-04-09 14:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('almoxarifado', '0007_alter_entrada_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
