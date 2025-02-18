# Generated by Django 5.0.7 on 2024-08-08 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Online_shop', '0007_category_slug_delete_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
