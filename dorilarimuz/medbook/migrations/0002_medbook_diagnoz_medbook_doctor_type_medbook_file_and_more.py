# Generated by Django 4.0.4 on 2022-06-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medbook',
            name='diagnoz',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medbook',
            name='doctor_type',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='medbook',
            name='file',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medbook',
            name='qr_code',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medbook',
            name='family',
            field=models.CharField(choices=[('F_M', 'Family Member'), ('Myself', 'myself')], max_length=256, verbose_name='Член Семьи'),
        ),
        migrations.AlterField(
            model_name='medbook',
            name='recept',
            field=models.ManyToManyField(null=True, to='medbook.recepts', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recepts',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]