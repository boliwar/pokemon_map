from django.db import models

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Pokemon', null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()