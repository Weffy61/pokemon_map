from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=False)
    title_jp = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    descr = models.TextField(max_length=400, null=False)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='next_evolution')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=False)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=False)
    disappeared_at = models.DateTimeField(null=False)
    level = models.IntegerField(null=False)
    health = models.IntegerField(null=False)
    strength = models.IntegerField(null=False)
    defence = models.IntegerField(null=False)
    stamina = models.IntegerField(null=False)

    def __str__(self):
        return self.pokemon.title_ru

