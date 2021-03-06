# Generated by Django 3.2.6 on 2021-09-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_image',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='participant',
            name='image_url',
            field=models.URLField(max_length=500),
        ),
    ]
