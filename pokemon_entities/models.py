from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    """Покемон."""
    title = models.CharField('Заголовок', max_length=200)
    title_en = models.CharField('Заголовок на английском', max_length=200, blank=True, default='')
    title_jp = models.CharField('Заголовок на японском', max_length=200, blank=True, default='')
    description = models.TextField('Описание', blank=True, default='')
    img = models.ImageField('Изображение', upload_to='Pokemon', null=True)
    previous_evolution = models.ForeignKey('self', related_name='next_evl', on_delete=models.PROTECT,
                                           blank=True, null=True, verbose_name='Предыдущая эволюция')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Свойства покемона."""
    pokemon = models.ForeignKey(Pokemon, related_name='pokemon_entities', on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота', )
    appeared_at = models.DateTimeField('Начало видимости', null=True)
    disappeared_at = models.DateTimeField('Окончание видимости', null=True)
    level = models.IntegerField('Уровень', default=1, blank=True)
    health = models.IntegerField('Здоровье', default=1, blank=True)
    attack = models.IntegerField('Атака', default=1, blank=True)
    protection = models.IntegerField('Защита', default=1, blank=True)
    endurance = models.IntegerField('Выносливость', default=1, blank=True)

    def __str__(self):
        return f'({self.lat}, {self.lon})[{self.appeared_at} - {self.disappeared_at}]'

