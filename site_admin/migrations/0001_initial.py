# Generated by Django 4.0.1 on 2022-05-03 08:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('unique_id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
    ]
