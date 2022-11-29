from django.db import models

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='Pokemon', null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    Level = models.IntegerField(default=1)
    Health = models.IntegerField(default=1)
    Attack = models.IntegerField(default=1)
    Protection = models.IntegerField(default=1)
    Endurance = models.IntegerField(default=1)
