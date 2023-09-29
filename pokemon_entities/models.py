from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя покемона')
    title_en = models.CharField(max_length=200, null=False, blank=True, verbose_name='Имя покемона на английском')
    title_jp = models.CharField(max_length=200, null=False, blank=True, verbose_name='Имя покемона на японском')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изобрадение')
    descr = models.TextField(max_length=400, null=False, blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='next_evolutions', verbose_name='Предыдущее поколение покемона')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Модель покемона')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title_ru

    class Meta:
        verbose_name = "Характеристики покемона"
        verbose_name_plural = "Характеристики покемонов"

