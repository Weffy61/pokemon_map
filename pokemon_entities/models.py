from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"
