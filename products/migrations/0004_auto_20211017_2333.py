# Generated by Django 3.2.8 on 2021-10-17 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='category',
            name='base_category_name',
        ),
    ]