# Generated by Django 3.2.3 on 2021-06-01 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='category/%Y/%m/%d'),
        ),
    ]
