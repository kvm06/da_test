# Generated by Django 3.2.8 on 2021-10-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usercoords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercoords',
            name='lat',
            field=models.FloatField(null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='usercoords',
            name='lng',
            field=models.FloatField(null=True, verbose_name='Долгота'),
        ),
    ]
