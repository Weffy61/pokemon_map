from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.lat, self.lon

