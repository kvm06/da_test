# Generated by Django 3.2.8 on 2021-10-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='base_category_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
