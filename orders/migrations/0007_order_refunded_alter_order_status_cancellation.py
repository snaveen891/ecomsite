# Generated by Django 5.1.5 on 2025-02-10 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Processing'), ('S', 'Shipped'), ('D', 'Delivered'), ('CR', 'Cancellation Requested'), ('C', 'Cancelled')], default='P', max_length=2),
        ),
        migrations.CreateModel(
            name='Cancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cancellations', to='orders.order')),
            ],
            options={
                'ordering': ('-created',),
                'indexes': [models.Index(fields=['created', 'updated'], name='orders_canc_created_c93c64_idx')],
            },
        ),
    ]
