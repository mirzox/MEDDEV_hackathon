# Generated by Django 4.0.4 on 2022-05-31 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_client_passport_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, verbose_name='phone number'),
        ),
    ]
