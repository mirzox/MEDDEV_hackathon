# Generated by Django 4.0.4 on 2022-06-04 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('medbook', '0002_medbook_diagnoz_medbook_doctor_type_medbook_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medbook',
            name='timestamp',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
