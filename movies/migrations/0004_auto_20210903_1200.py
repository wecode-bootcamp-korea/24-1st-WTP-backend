# Generated by Django 3.2.6 on 2021-09-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_participant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster_image',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
