# Generated by Django 2.1.1 on 2018-10-14 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20181013_1124'),
        ('resource', '0008_products_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.Info'),
        ),
    ]
