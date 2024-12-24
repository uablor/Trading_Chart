# Generated by Django 5.1.3 on 2024-12-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='balance',
            new_name='real_balance',
        ),
        migrations.AddField(
            model_name='wallet',
            name='demo_balance',
            field=models.IntegerField(default=1000),
        ),
    ]