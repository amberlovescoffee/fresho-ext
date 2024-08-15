# Generated by Django 5.0.7 on 2024-08-15 06:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_parent_order_id_alter_deliveryrun_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, db_comment='UTC', default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_comment='UTC', default=django.utils.timezone.now, null=True),
        ),
    ]
