# Generated by Django 4.2.15 on 2025-01-05 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_api', '0002_rename_profile_id_product_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
