# Generated by Django 4.2 on 2023-04-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almoxarifado', '0003_entrada_number_alter_entrada_total_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destiny', models.CharField(max_length=255)),
                ('date_create', models.DateField()),
                ('requester', models.CharField(max_length=255)),
            ],
        ),
    ]
