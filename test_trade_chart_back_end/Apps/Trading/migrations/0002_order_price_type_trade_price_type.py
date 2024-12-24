# Generated by Django 5.1.3 on 2024-12-20 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price_type',
            field=models.CharField(blank=True, choices=[('real_price', 'real_price'), ('demo_price', 'demo_price')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='price_type',
            field=models.CharField(blank=True, choices=[('real_price', 'real_price'), ('demo_price', 'demo_price')], max_length=100, null=True),
        ),
    ]