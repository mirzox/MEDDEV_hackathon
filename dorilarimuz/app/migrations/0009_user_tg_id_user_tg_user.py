# Generated by Django 4.0.4 on 2022-06-04 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_doctortypechoices_doctortype'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tg_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='tg_user',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
