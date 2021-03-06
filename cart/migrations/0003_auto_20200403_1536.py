# Generated by Django 3.0.5 on 2020-04-03 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20200403_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_item',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
