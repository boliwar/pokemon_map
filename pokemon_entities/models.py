from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    """Покемон."""
    id = models.AutoField('Ид', primary_key=True)
    title = models.CharField('Заголовок', max_length=200)
    title_en = models.CharField('Заголовок на английском', max_length=200, blank=True, null=True)
    title_jp = models.CharField('Заголовок на японском', max_length=200, blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    img = models.ImageField('Изображение', upload_to='Pokemon', null=True)
    previous_evolution = models.ForeignKey('self', related_name='next_evl', on_delete=models.PROTECT,
                                           blank=True, null=True, verbose_name='Предыдущая эволюция')
    # next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Свойства покемона."""
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1, verbose_name='Покемон')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота', )
    appeared_at = models.DateTimeField('Начало видимости', null=True)
    disappeared_at = models.DateTimeField('Окончание видимости', null=True)
    Level = models.IntegerField('Уровень', default=1, blank=True)
    Health = models.IntegerField('Здоровье', default=1, blank=True)
    Attack = models.IntegerField('Атака', default=1, blank=True)
    Protection = models.IntegerField('Защита', default=1, blank=True)
    Endurance = models.IntegerField('Выносливость', default=1, blank=True)

    def __str__(self):
        return f'({self.lat}, {self.lon})[{self.appeared_at} - {self.disappeared_at}]'

