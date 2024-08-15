# Generated by Django 5.0.7 on 2024-08-15 05:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_deliveryrun_options_alter_deliveryrun_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='parent_order_id',
            field=models.UUIDField(blank=True, db_comment="indicate if it's a backorder", null=True),
        ),
        migrations.AlterField(
            model_name='deliveryrun',
            name='created_at',
            field=models.DateTimeField(blank=True, db_comment='UTC', default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryrun',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_comment='UTC', default=django.utils.timezone.now, null=True),
        ),
    ]
