# Generated by Django 3.1.14 on 2022-11-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20221129_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='img',
            field=models.ImageField(null=True, upload_to='Pokemon'),
        ),
    ]