# Generated by Django 5.0.3 on 2024-04-03 02:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auction_details_bids_winningbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_bids', to='base.products'),
        ),
    ]
