# Generated by Django 3.1.14 on 2022-12-02 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0026_auto_20221202_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='attack',
            field=models.IntegerField(blank=True, verbose_name='Атака'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='endurance',
            field=models.IntegerField(blank=True, verbose_name='Выносливость'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='health',
            field=models.IntegerField(blank=True, verbose_name='Здоровье'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='level',
            field=models.IntegerField(blank=True, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='protection',
            field=models.IntegerField(blank=True, verbose_name='Защита'),
        ),
    ]