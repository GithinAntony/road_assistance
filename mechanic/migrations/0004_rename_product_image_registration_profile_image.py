# Generated by Django 4.0.1 on 2022-05-03 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic', '0003_registration_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='product_image',
            new_name='profile_image',
        ),
    ]
