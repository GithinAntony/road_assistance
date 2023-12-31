# Generated by Django 4.0.1 on 2022-05-03 10:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('site_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('unique_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
    ]
