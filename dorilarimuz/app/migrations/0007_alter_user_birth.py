# Generated by Django 4.0.4 on 2022-06-03 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_delete_client_user_birth_user_passport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год рождения'),
        ),
    ]
