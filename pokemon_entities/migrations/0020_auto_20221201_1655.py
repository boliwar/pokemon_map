# Generated by Django 3.1.14 on 2022-12-01 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0019_auto_20221129_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]